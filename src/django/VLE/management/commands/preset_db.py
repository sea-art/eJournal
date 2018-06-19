from django.core.management.base import BaseCommand
from VLE.models import *
from VLE.factory import *
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    help = 'Generates useful data for the database.'

    def gen_users(self):
        users_examples = [
            {"username": "Lars", "pass": "pass"},
            {"username": "Rick", "pass": "pass"},
            {"username": "Dennis", "pass": "pass"},
            {"username": "Zi", "pass": "pass"},
            {"username": "Jeroen", "pass": "pass"},
            {"username": "Maarten", "pass": "pass"}
        ]

        self.users = []
        for u in users_examples:
            self.users.append(make_user(u['username'], u['pass']))

    def gen_roles(self):
        role_examples = [
            {"name": "Student"},
            {"name": "TA"},
            {"name": "Teacher"}
        ]

        self.roles = []
        for r in role_examples:
            self.roles.append(make_role(r["name"]))

    def gen_courses(self):
        courses_examples = [
            {
                "name": "Portfolio Academische Vaardigheden 1",
                "abbr": "PAV",
                "students": [0, 1, 2],
                "teachers": [3, 4, 5],
            },
            {
                "name": "Portfolio Academische Vaardigheden 2",
                "abbr": "PAV",
                "students": [0, 1, 2],
                "teachers": [3, 4, 5],
            },
            {
                "name": "Beeldbewerken",
                "abbr": "BB",
                "students": [0, 1, 2, 3, 4, 5],
                "teachers": [0],
            },
            {
                "name": "Automaten en Formele Talen",
                "abbr": "AFT",
                "students": [],
                "teachers": [0, 1, 2, 3, 4, 5],
            }
        ]

        self.courses = []
        for c in courses_examples:
            startdate = faker.date_this_decade(before_today=True)
            course = make_course(c["name"], c["abbr"], startdate, self.users[random.choice(c["teachers"])])

            for sid in c["students"]:
                student = self.users[sid]
                make_participation(student, course, self.roles[0])

            self.courses.append(course)

    def gen_templates(self):
        template_examples = [
            {
                "name": "Colloquium",
                "fields": [
                    {"title": "Title", "location": 0, "type": Field.TEXT},
                    {"title": "Summary", "location": 1, "type": Field.TEXT},
                    {"title": "Experience", "location": 2, "type": Field.TEXT},
                    {"title": "Proof", "location": 3, "type": Field.IMG},
                ]
            },
            {
                "name": "Default Text",
                "fields": [
                    {"title": "Text", "location": 0, "type": Field.TEXT},
                ]
            },
            {
                "name": "Default Image",
                "fields": [
                    {"title": "Image", "location": 0, "type": Field.IMG},
                ]
            },
            {
                "name": "Default File",
                "fields": [
                    {"title": "File", "location": 0, "type": Field.FILE},
                ]
            },
        ]

        self.templates = []
        for t in template_examples:
            template = make_entry_template(t["name"])
            for f in t["fields"]:
                make_field(template, f["title"], f["location"], f["type"])

            self.templates.append(template)

    def gen_format(self):
        format_examples = [
            {
                "templates": [1, 2, 3],
                "presets": [
                    {"type": Node.PROGRESS, "points": 10},
                ]
            },
            {
                "templates": [0],
                "presets": [
                    {"type": Node.PROGRESS, "points": 5},
                    {"type": Node.ENTRYDEADLINE, "template": 1},
                ]
            },
            {
                "templates": [],
                "presets": [
                    {"type": Node.ENTRYDEADLINE, "template": 1},
                    {"type": Node.ENTRYDEADLINE, "template": 0},
                    {"type": Node.ENTRYDEADLINE, "template": 1},
                ]
            },
        ]

        self.formats = []
        for f in format_examples:
            templates = [self.templates[template] for template in f["templates"]]
            format = make_format(templates)

            for p in f["presets"]:
                deadline_date = faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)

                if p["type"] == Node.PROGRESS:
                    deadline = make_deadline(deadline_date, p["points"])
                    preset = make_progress_node(format, deadline)
                elif p["type"] == Node.ENTRYDEADLINE:
                    deadline = make_deadline(deadline_date)
                    preset = make_entrydeadline_node(format, deadline, self.templates[p["template"]])

            self.formats.append(format)

    def gen_assignments(self):
        assign_examples = [
            {
                "name": "Logboek",
                "description": "This is a logboek for all your logging purposes",
                "courses": [0, 1, 2, 3],
                "format": 0,
                "author": 4,
            },
            {
                "name": "Colloquium",
                "description": "This is the best colloquium logbook in the world",
                "courses": [0],
                "format": 1,
                "author": 4,
            },
            {
                "name": "Verslag",
                "description": "Verslag your verslag",
                "courses": [0, 1],
                "format": 2,
                "author": 4,
            },
        ]

        self.assignments = []
        for a in assign_examples:
            author = self.users[a["author"]]
            format = self.formats[a["format"]]
            deadline = faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)
            assignment = make_assignment(a["name"], a["description"], author, format, deadline)

            for course in a["courses"]:
                assignment.courses.add(self.courses[course])
            self.assignments.append(assignment)

    def gen_journals(self):
        journal_examples = [
            {"assignment": 0, "users": [0, 1, 2, 3, 4]},
            {"assignment": 1, "users": [0, 5, 6, 7, 8]},
            {"assignment": 2, "users": [6, 7, 8]},
        ]

        self.journals = []
        for a in self.assignments:
            for u in self.users:
                journal = make_journal(a, u)
                self.journals.append(journal)

    def gen_entries(self):
        for journal in self.journals:
            for node in journal.node_set.all():
                if node.type == Node.ENTRYDEADLINE:
                    if random.randint(0, 2) > 0:
                        continue

                    entry = make_entry(node.preset.forced_template, faker.date_time_this_month(before_now=True))
                    entry.late = faker.boolean()
                    entry.grade = random.randint(1, 10)
                    entry.save()

                    node.entry = entry

            if journal.assignment.format.available_templates.count() > 0:
                random_entries = random.randint(0, 8)
                for _ in range(random_entries):
                    template = random.choice(journal.assignment.format.available_templates.all())
                    entry = make_entry(template, faker.date_time_this_month(before_now=True))
                    entry.late = faker.boolean()
                    entry.grade = random.randint(1, 10)
                    entry.save()

                    make_node(journal, entry)

    def gen_content(self):
        for journal in self.journals:
            for node in journal.node_set.all():
                if node.type == Node.ENTRY or node.type == Node.ENTRYDEADLINE:
                    if node.entry is None:
                        continue

                    template = node.entry.template
                    for field in template.field_set.all():
                        content = make_content(node.entry, faker.catch_phrase(), field)

    def handle(self, *args, **options):
        """
        This function generates data to test and fill the database with.
        This only contains the 'useful data'. For random data, execute demo_db as well.
        """
        self.gen_users()
        self.gen_roles()
        self.gen_courses()
        self.gen_templates()
        self.gen_format()
        self.gen_assignments()
        self.gen_journals()
        self.gen_entries()
        self.gen_content()
