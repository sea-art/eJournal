"""
Generate preset data.

Generate preset data and save it to the database.
"""

import datetime
import random

from django.core.management.base import BaseCommand
from faker import Faker

import VLE.factory as factory
from VLE.models import Course, Field, Node

faker = Faker()


class Command(BaseCommand):
    """Generate preset data and save it to the database."""

    help = 'Generates useful data for the database.'

    def gen_users(self):
        """Generate users with password 'pass'."""
        users_examples = {
            "Student": {
                "username": "Student",
                "full_name": "Lars van Hijfte",
                "verified_email": True,
                "password": "pass",
                "email": "lars@eJourn.al",
                "is_superuser": False,
                "is_teacher": False
            },
            "Student2": {
                "username": "Student2",
                "full_name": "Rick Watertor",
                "verified_email": True,
                "password": "pass",
                "email": "rick@eJourn.al",
                "is_superuser": False,
                "is_teacher": False
            },
            "Student3": {
                "username": "Student3",
                "full_name": "Dennis Wind",
                "password": "pass",
                "email": "dennis@eJourn.al",
                "verified_email": True,
                "is_superuser": False,
                "is_teacher": False
            },
            "Student4": {
                "username": "Student4",
                "full_name": "Maarten Keulen",
                "password": "pass",
                "email": "maarten@eJourn.al",
                "verified_email": False,
                "is_superuser": False,
                "is_teacher": False
            },
            "Student5": {
                "username": "Student5",
                "full_name": "Zi Long Zhu",
                "password": "pass",
                "email": "zi@eJourn.al",
                "verified_email": False,
                "is_superuser": False,
                "is_teacher": False
            },
            "Teacher": {
                "username": "Teacher",
                "full_name": "Xavier van Dommelen",
                "password": "pass",
                "email": "test@eJourn.al",
                "verified_email": True,
                "is_superuser": False,
                "is_teacher": True
            },
            "TA": {
                "username": "TA",
                "full_name": "De TA van TAing",
                "verified_email": False,
                "password": "pass",
                "email": "ta@eJourn.al",
                "is_superuser": False,
                "is_teacher": False
            },
            "TA2": {
                "username": "TA2",
                "full_name": "Backup TA van TAing",
                "verified_email": False,
                "password": "pass",
                "email": "ta2@eJourn.al",
                "is_superuser": False,
                "is_teacher": False
            },
            "Superuser": {
                "username": "Superuser",
                "full_name": "Super User",
                "password": "pass",
                "email": "superuser@eJourn.al",
                "verified_email": False,
                "is_superuser": True,
                "is_teacher": True,
                "is_staff": True
            }
        }

        self.users = {}

        for key, value in users_examples.items():
            self.users[key] = factory.make_user(**value)

    def gen_courses(self):
        """Generate courses."""
        courses_examples = {
            "Portfolio Academische Vaardigheden 1": {
                "pk": 1697,
                "name": "Portfolio Academische Vaardigheden 1",
                "abbr": "PAV1",
                "author": self.users["Teacher"],
                "students": [self.users[s] for s in ["Student", "Student2", "Student3", "Student4", "Student5"]],
                "teachers": [self.users["Teacher"]],
                "tas": [self.users["TA"]],
                "start_date": faker.date("2018-09-01"),
                "end_date": faker.date("2019-09-01"),
                "student_group_names": ["Cobol", "Smalltalk"]
            },
            "Portfolio Academische Vaardigheden 2": {
                "pk": 1698,
                "name": "Portfolio Academische Vaardigheden 2",
                "abbr": "PAV2",
                "author": self.users["Teacher"],
                "students": [self.users[s] for s in ["Student", "Student2", "Student3", "Student4", "Student5"]],
                "teachers": [self.users["Teacher"]],
                "tas": [self.users["TA2"]],
                "start_date": faker.date("2018-09-01"),
                "end_date": faker.date("2019-09-01"),
                "student_group_names": ["Algol", "Ruby"]
            }
        }

        self.courses = {}
        for c in courses_examples.values():
            course = Course(pk=c["pk"], name=c["name"], abbreviation=c["abbr"], startdate=c["start_date"],
                            enddate=c["end_date"], author=c["author"])
            course.save()

            student_groups = [factory.make_course_group(g, course) for g in c["student_group_names"]]
            staff_group = factory.make_course_group("Staff", course)

            role_student = factory.make_role_student('Student', course)
            role_ta = factory.make_role_ta('TA', course)
            role_teacher = factory.make_role_teacher('Teacher', course)

            for student in c["students"]:
                factory.make_participation(student, course, role_student, random.choice(student_groups))
            for ta in c["tas"]:
                factory.make_participation(ta, course, role_ta, random.choice(student_groups))
            for teacher in c["teachers"]:
                factory.make_participation(teacher, course, role_teacher, staff_group)

            self.courses[c["name"]] = course

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
                    {"title": "Summary", "location": 1, "type": Field.RICH_TEXT},
                    {"title": "Experience", "location": 2, "type": Field.RICH_TEXT},
                    {"title": "Requested Points", "location": 3, "type": Field.TEXT},
                ]
            },
            {
                "name": "Default Text",
                "fields": [
                    {"title": "Text", "location": 0, "type": Field.TEXT},
                ]
            }
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
                "templates": [0, 1],
                "presets": [
                    {"type": Node.PROGRESS, "points": 10},
                ]
            },
            {
                "templates": [0],
                "presets": [
                    {"type": Node.PROGRESS, "points": 5},
                    {"type": Node.PROGRESS, "points": 1, "description": "1 day", "deadline_days": 1},
                    {"type": Node.PROGRESS, "points": 3, "description": "1 week", "deadline_days": 7},
                    {"type": Node.ENTRYDEADLINE, "template": 1, "description": "1 week entrydl", "deadline_days": 7},
                    {"type": Node.ENTRYDEADLINE, "template": 1},
                ]
            },
        ]

        self.formats = []
        for f in format_examples:
            templates = [self.templates[template] for template in f["templates"]]
            format = factory.make_format(templates)

            for p in f["presets"]:
                if "deadline_days" in p:
                    deadline_date = datetime.datetime.utcnow() + datetime.timedelta(days=p["deadline_days"])
                else:
                    deadline_date = faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)

                if p["type"] == Node.PROGRESS:
                    node = factory.make_progress_node(format, deadline_date, p["points"])
                    if "description" in p:
                        node.description = p["description"]
                        node.save()
                elif p["type"] == Node.ENTRYDEADLINE:
                    factory.make_entrydeadline_node(format, deadline_date, self.templates[p["template"]])

            self.formats.append(format)

    def gen_assignments(self):
        """Generate assignments."""
        assign_examples = [
            {
                "name": "Logboek",
                "description": "This is a logboek for all your logging purposes",
                "courses": [
                    self.courses["Portfolio Academische Vaardigheden 1"],
                    self.courses["Portfolio Academische Vaardigheden 2"]
                ],
                "format": 0,
                "author": self.users["Teacher"],
            },
            {
                "name": "Colloquium",
                "description": "This is the best colloquium logbook in the world",
                "courses": [self.courses["Portfolio Academische Vaardigheden 1"]],
                "format": 1,
                "author": self.users["Teacher"],
            }
        ]

        self.assignments = []
        for a in assign_examples:
            format = self.formats[a["format"]]
            faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)
            assignment = factory.make_assignment(a["name"], a["description"], a["author"], format, is_published=True)

            for course in a["courses"]:
                assignment.courses.add(course)
            self.assignments.append(assignment)

    def gen_journals(self):
        """Generate journals."""
        self.journals = []
        for a in self.assignments:
            for u in self.users.values():
                journal = factory.make_journal(a, u)
                self.journals.append(journal)

    def gen_entries(self):
        """Generate entries."""
        for journal in self.journals:
            for node in journal.node_set.all():
                if node.type == Node.ENTRYDEADLINE:
                    entry = factory.make_entry(node.preset.forced_template)
                    entry.late = faker.boolean()
                    entry.grade = random.randint(1, 10)
                    entry.save()

                    node.entry = entry

            if journal.assignment.format.available_templates.count() > 0:
                random_entries = random.randint(0, 8)
                for _ in range(random_entries):
                    template = random.choice(journal.assignment.format.available_templates.all())
                    entry = factory.make_entry(template)
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
                        if field.type in [Field.TEXT, Field.RICH_TEXT]:  # Files requires the actual file...
                            if "Requested Points" in field.title:
                                factory.make_content(node.entry, str(random.randint(1, 3)), field)
                            else:
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
