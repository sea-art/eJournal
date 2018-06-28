"""
Demo generate script.

A script that generates demo data.
It generates a teacher and student account. The teacher has permissions.
"""

from django.core.management.base import BaseCommand
from VLE.models import Field, Node, Role
import VLE.factory as factory
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    """Generates data for the database for the demo."""

    help = 'Generates useful data for the database.'

    def gen_users(self):
        """Generate a student and teacher."""
        users_examples = [
            {"username": "Student", "pass": "pass", "is_admin": False},
            {"username": "Teacher", "pass": "pass", "is_admin": False},
            {"username": "Admin", "pass": "pass", "is_admin": True},
        ]

        self.users = []
        for u in users_examples:
            self.users.append(factory.make_user(u['username'], u['pass'], is_admin=u['is_admin']))

    def gen_courses(self):
        """Generate the courses PAV and Beeldbewerken."""
        courses_examples = [
            {
                "name": "Portfolio Academische Vaardigheden 1",
                "abbr": "PAV",
                "students": [0],
                "teachers": [1],
            },
            {
                "name": "Beeldbewerken",
                "abbr": "BB",
                "students": [0],
                "teachers": [1],
            }
        ]
        self.courses = []
        for c in courses_examples:
            startdate = faker.date_this_decade(before_today=True)
            enddate = faker.date_this_decade(before_today=False)
            course = factory.make_course(c["name"], c["abbr"], startdate, enddate, self.users[random.choice(c["teachers"])])
            role = Role.objects.get(name='Student', course=course)
            for sid in c["students"]:
                student = self.users[sid]
                factory.make_participation(student, course, role)

            self.courses.append(course)

    def gen_templates(self):
        """Generate templates.

        One with title, summary, experience and requested points.
        One with only a title.
        """
        template_examples = [
            {
                "name": "Colloquium",
                "fields": [
                    {"title": "Title", "location": 0, "type": Field.TEXT},
                    {"title": "Summary", "location": 1, "type": Field.TEXT},
                    {"title": "Experience", "location": 2, "type": Field.TEXT},
                    {"title": "Requested Points", "location": 3, "type": Field.TEXT},
                ]
            },
            {
                "name": "Beeldbewerken Cijfers",
                "fields": [
                    {"title": "Text", "location": 0, "type": Field.TEXT},
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
        """Generate a assignment format."""
        format_examples = [
            {
                "templates": [1],
                "presets": [
                    {"type": Node.PROGRESS, "points": 5}
                ]
            },
            {
                "templates": [0],
                "presets": [
                    {"type": Node.PROGRESS, "points": 5},
                    {"type": Node.PROGRESS, "points": 10}
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
                "name": "Colloquium",
                "description": "This is the best colloquium logbook in the world",
                "courses": [0],
                "format": 1,
                "author": 1,
            },
            {
                "name": "Verslag",
                "description": "Verslag your verslag",
                "courses": [1],
                "format": 0,
                "author": 1,
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
