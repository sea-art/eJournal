"""
Generate preset data.

Generate preset data and save it to the database.
"""

from django.core.management.base import BaseCommand
from VLE.models import Field, Node, Role
import VLE.factory as factory
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    """Generate preset data and save it to the database."""

    help = 'Generates useful data for the database.'

    def gen_users(self):
        """Generate users with password 'pass'."""
        users_examples = [
            {
                "username": "22222222",
                "first_name": "Lars",
                "last_name": "van Hijfte",
                "pass": "pass",
                "is_admin": False,
                "is_teacher": False
            }, {
                "username": "11111111",
                "first_name": "Rick",
                "last_name": "Watertor",
                "pass": "pass",
                "is_admin": False,
                "is_teacher": False
            }, {
                "username": "00000000",
                "first_name": "Dennis",
                "last_name": "Wind",
                "pass": "pass",
                "is_admin": False,
                "is_teacher": False
            }, {
                "username": "33333333",
                "first_name": "Maarten",
                "last_name": "Keulen",
                "pass": "pass",
                "is_admin": True,
                "is_teacher": False
            }, {
                "username": "44444444",
                "first_name": "Zi Long",
                "last_name": "Zhu",
                "pass": "pass",
                "is_admin": False,
                "is_teacher": False
            }, {
                "username": "55555555",
                "first_name": "Xavier",
                "last_name": "van Dommelen",
                "pass": "pass",
                "is_admin": False,
                "is_teacher": True
            }
        ]

        self.users = []
        for u in users_examples:
            is_admin = False
            is_teacher = False
            if u['is_admin']:
                is_admin = True
            if u['is_teacher']:
                is_teacher = True
            self.users.append(factory.make_user(u['username'], u['pass'], is_superuser=is_admin, is_teacher=is_teacher,
                                                first_name=u['first_name'], last_name=u['last_name']))

    def gen_courses(self):
        """Generate courses."""
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
                "students": [1, 2, 3, 4, 5],
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
            enddate = faker.date_this_decade(before_today=False)
            author = self.users[random.choice(c["teachers"])]
            course = factory.make_course(c["name"], c["abbr"], startdate, enddate, author)
            role_teacher = Role.objects.get(name='Teacher', course=course)
            role_student = Role.objects.get(name='Student', course=course)
            for sid in c["students"]:
                student = self.users[sid]
                factory.make_participation(student, course, role_student)
            for cid in c["teachers"]:
                if self.users[cid] == author:
                    continue
                teacher = self.users[cid]
                factory.make_participation(teacher, course, role_teacher)

            self.courses.append(course)

    def gen_templates(self):
        """Generate templates.

        One with title, summary, experience, requested points and proof.
        One with only a title.
        One with only an image.
        One with only a file.
        """
        template_examples = [
            {
                "name": "Colloquium",
                "fields": [
                    {"title": "Title", "location": 0, "type": Field.TEXT},
                    {"title": "Summary", "location": 1, "type": Field.TEXT},
                    {"title": "Experience", "location": 2, "type": Field.TEXT},
                    {"title": "Requested Points", "location": 3, "type": Field.TEXT},
                    {"title": "Proof", "location": 4, "type": Field.IMG},
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
            template = factory.make_entry_template(t["name"])
            for f in t["fields"]:
                factory.make_field(template, f["title"], f["location"], f["type"])

            self.templates.append(template)

    def gen_format(self):
        """Generate a format."""
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
            format = factory.make_format(templates)

            for p in f["presets"]:
                deadline_date = faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)

                if p["type"] == Node.PROGRESS:
                    factory.make_progress_node(format, deadline_date, p["points"])
                elif p["type"] == Node.ENTRYDEADLINE:
                    factory.make_entrydeadline_node(format, deadline_date, self.templates[p["template"]])

            self.formats.append(format)

    def gen_assignments(self):
        """Generate assignments."""
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
            faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)
            assignment = factory.make_assignment(a["name"], a["description"], author, format)

            for course in a["courses"]:
                assignment.courses.add(self.courses[course])
            self.assignments.append(assignment)

    def gen_journals(self):
        """Generate journals."""
        self.journals = []
        for a in self.assignments:
            for u in self.users:
                journal = factory.make_journal(a, u)
                self.journals.append(journal)

    def gen_entries(self):
        """Generate entries."""
        for journal in self.journals:
            for node in journal.node_set.all():
                if node.type == Node.ENTRYDEADLINE:
                    if random.randint(0, 2) > 0:
                        continue

                    entry = factory.make_entry(node.preset.forced_template, faker.date_time_this_month(before_now=True))
                    entry.late = faker.boolean()
                    entry.grade = random.randint(1, 10)
                    entry.save()

                    node.entry = entry

            if journal.assignment.format.available_templates.count() > 0:
                random_entries = random.randint(0, 8)
                for _ in range(random_entries):
                    template = random.choice(journal.assignment.format.available_templates.all())
                    entry = factory.make_entry(template, faker.date_time_this_month(before_now=True))
                    entry.late = faker.boolean()
                    entry.grade = random.randint(1, 10)
                    entry.save()

                    factory.make_node(journal, entry)

    def gen_content(self):
        """Generate content for an entry."""
        for journal in self.journals:
            for node in journal.node_set.all():
                if node.type == Node.ENTRY or node.type == Node.ENTRYDEADLINE:
                    if node.entry is None:
                        continue

                    template = node.entry.template
                    for field in template.field_set.all():
                        factory.make_content(node.entry, faker.catch_phrase(), field)

    def handle(self, *args, **options):
        """Generate data to test and fill the database with.

        This only contains the 'useful data'. For random data, execute demo_db as well.
        """
        self.gen_users()
        self.gen_courses()
        self.gen_templates()
        self.gen_format()
        self.gen_assignments()
        self.gen_journals()
        self.gen_entries()
        self.gen_content()
