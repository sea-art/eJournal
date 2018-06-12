from django.core.management.base import BaseCommand
from VLE.models import *
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    help = 'Generates data for the database.'

    def gen_prepared_data(self, ):
        """Generate useful data to test with.

        These are preselected users and are assigned to courses to run tests with.
        """
        users_examples = [
            {"username": "Lars", "type": "SD"},
            {"username": "Rick", "type": "SD"},
            {"username": "Dennis", "type": "SD"},
            {"username": "Zi", "type": "TA"},
            {"username": "Jeroen", "type": "TE"},
            {"username": "Maarten", "type": "SU"}
        ]
        courses_examples = [
            {"name": "Portofolio Academische Vaardigheden 1", "abbr": "PAV"},
            {"name": "Portofolio Academische Vaardigheden 2", "abbr": "PAV"},
            {"name": "Beeldbewerken", "abbr": "BB"},
            {"name": "Automaten en Formele Talen", "abbr": "AFT"}
        ]
        assign_examples = [
            {"name": "Logboek", "courses": [0, 1, 2, 3]},
            {"name": "colloquium", "courses": [0]},
            {"name": "Verslag", "courses": [0, 1]},
        ]
        journal_examples = [
            {"assigns": 0, "users": 0},
            {"assigns": 1, "users": 2},
        ]

        users = []
        for u in users_examples:
            user = User(username=u["username"], group=u["type"])
            user.set_password('pass')
            user.save()
            users.append(user)

        courses = []
        for c in courses_examples:
            course = Course(name=c["name"], abbreviation=c["abbr"])
            course.save()
            course.authors.add(users[2])
            course.authors.add(users[3])
            courses.append(course)

        assignments = []
        for a in assign_examples:
            assignment = Assignment(name=a["name"])
            assignment.save()
            for course in a["courses"]:
                assignment.courses.add(courses[course])
            assignments.append(assignment)

        journals = []
        for j in journal_examples:
            journal = Journal(assignment=assignments[j["assigns"]], user=users[j["users"]])
            journal.save()

    def gen_random_users(self, amount):
        """
        Generate random users.
        """
        for _ in range(amount):
            user = User()
            groups = [x[0] for x in user._meta.get_field('group').choices]
            user.group = random.choice(groups)
            user.email = faker.ascii_safe_email()

            used_names = User.objects.all().values('username')
            user.username = faker.name()
            counter = 0
            while(user.username in used_names and counter < 10000):
                user.username = faker.name()
                counter += 1
            if counter == 10000:
                print("Could not find unique username")
                exit()

            user.set_password(faker.password())
            user.education = faker.sentence()
            user.lti_id = faker.random_int()
            user.save()

    def gen_random_courses(self, amount):
        """
        Generate random courses.
        """
        for _ in range(amount):
            course = Course()
            course.save()
            course.name = faker.company()

            teachers = User.objects.filter(group='TE')
            teacher_amount = random.randint(1, 3)
            if len(teachers) > 0:
                for author in random.choices(teachers, k=teacher_amount):
                    course.authors.add(author)

            students = User.objects.all().filter(group='SD')
            for student in students[:min(50, len(students))]:
                course.participants.add(student)

            TAs = User.objects.all().filter(group='TA')
            TA_amount = random.randint(2, 7)
            if len(TAs) > 0:
                for TA in random.choices(TAs, k=TA_amount):
                    course.TAs.add(TA)

            course.abbrevation = random.choices(course.name, k=4)
            course.startdate = faker.date_this_decade(before_today=True)
            course.save()

    def gen_random_assignments(self, amount):
        """
        Generate random assignments.
        """
        for _ in range(amount):
            if Course.objects.all().count() == 0:
                continue
            assignment = Assignment()
            assignment.save()
            assignment.name = faker.catch_phrase()
            assignment.description = faker.paragraph()
            courses = Course.objects.all()
            for course in random.choices(courses, k=3):
                if assignment.courses.count():
                    assignment.courses.add(course)
                else:
                    if random.randint(1, 101) > 70:
                        assignment.courses.add(course)
            assignment.save()

    def gen_random_journals(self, amount):
        """
        Generate random journals.
        """
        for _ in range(amount):
            if Assignment.objects.all().count() == 0:
                continue
            journal = Journal()
            journal.assignment = random.choice(Assignment.objects.all())
            journal.user = random.choice(User.objects.all())
            journal.save()

    def gen_random_entries(self, amount):
        """
        Generate random entries.
        """
        for _ in range(amount):
            if Journal.objects.all().count() == 0:
                continue
            entry = Entry()
            entry.journal = random.choice(Journal.objects.all())
            entry.datetime = faker.date_time_this_month(before_now=True)
            entry.late = faker.boolean()
            entry.save()

    def handle(self, *args, **options):
        """This function generates data to test and fill the database with.

        It has both useful test data and randomly created data to create a more real life example.
        """
        # Preselected items
        self.gen_prepared_data()

        amount = 10
        # Random users
        self.gen_random_users(amount)
        # Random course
        self.gen_random_courses(amount)
        # Random assignments
        self.gen_random_assignments(amount)
        # Random journals
        self.gen_random_journals(amount)
        # Random entries
        self.gen_random_entries(amount)
