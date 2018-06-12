from django.core.management.base import BaseCommand
from VLE.models import *
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    help = 'Generates random data for the database.'

    def handle(self, *args, **options):
        amount = 10
        # User
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
            print("user: ", user)
            user.save()

        # Course
        for _ in range(amount):
            course = Course()
            course.save()
            course.name = faker.company()

            teachers = User.objects.filter(group='TE')
            teacher_amount = random.randint(1, 3)
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
            print("course: ", course)
            course.save()

        # Assignment
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
            print("assignment: ", assignment)
            assignment.save()

        # Journal
        for _ in range(amount):
            if Assignment.objects.all().count() == 0:
                continue
            journal = Journal()
            journal.assignment = random.choice(Assignment.objects.all())
            journal.user = random.choice(User.objects.all())
            print("journal: ", journal)
            journal.save()

        # Entry
        for _ in range(amount):
            if Journal.objects.all().count() == 0:
                continue
            entry = Entry()
            entry.journal = random.choice(Journal.objects.all())
            entry.datetime = faker.date_time_this_month(before_now=True)
            entry.late = faker.boolean()
            entry.save()
            print("entry: ", entry)
