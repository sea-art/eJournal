"""
Generate test data.

Generate an extensive set of data and save it to the database.
"""
from django.core.management.base import BaseCommand
from VLE.models import Entry, User, Role, Course, Participation, JournalFormat, Assignment, Journal
import VLE.factory as factory
from faker import Faker
import random
faker = Faker()


class Command(BaseCommand):
    """Generates data for the database."""

    help = 'Generates data for the database.'

    def gen_random_content(self):
        """Generate random content."""
        entries = Entry.objects.all()
        for i, entry in enumerate(entries):
            for field in entry.template.field_set.all():
                # Randomly miss content fields for testing.
                if random.randint(0, 20) == 0:
                    continue

                content = factory.make_content(entry, faker.catch_phrase(), field)
                content.save()

    def gen_random_users(self, amount):
        """Generate random users."""
        used_email = [email['email'] for email in User.objects.all().values('email')]
        used_names = [email['username'] for email in User.objects.all().values('username')]
        used_lti = [email['lti_id'] for email in User.objects.all().values('lti_id')]

        for _ in range(amount):
            user = User()
            # Generate unique email or exit.
            user.email = faker.ascii_safe_email()
            counter = 0
            while(user.email in used_email and counter < 10000):
                user.email = faker.ascii_safe_email()
                counter += 1
            if counter == 10000:
                print("Could not find unique email")
                exit()

            # Generate unique name or exit.
            user.username = faker.name()
            counter = 0
            while(user.username in used_names and counter < 10000):
                user.username = faker.name()
                counter += 1
            if counter == 10000:
                print("Could not find unique username")
                exit()

            user.set_password(faker.password())
            user.profile_picture = '/static/oh_no/{}.png'.format(random.randint(1, 10))

            # Generate unique lti_id.
            user.lti_id = faker.name()
            counter = 0
            while(user.lti_id in used_lti and counter < 10000):
                user.lti_id = faker.name()
                counter += 1
            if counter == 10000:
                print("Could not find unique lti_id")
                exit()

            user.save()
            used_email.append(user.email)
            used_names.append(user.username)
            used_lti.append(user.lti_id)

    def gen_random_courses(self, amount):
        """Generate random courses."""
        for _ in range(amount):
            course = Course()
            course.save()
            course.name = faker.company()

            teachers = User.objects.all()
            if len(teachers) > 0:
                course.author = random.choice(teachers)

            course.abbrevation = random.choices(course.name, k=4)
            course.startdate = faker.date_this_decade(before_today=True)
            course.save()

    def gen_roles(self):
        """Generate roles for participation in courses."""
        ta = Role()
        ta.name = "TA"

        ta.can_edit_grades = True
        ta.can_view_grades = True
        ta.can_edit_assignment = True
        ta.can_view_assignment = True
        ta.can_submit_assignment = True
        ta.save()

        student = Role()
        student.name = "student"

        student.can_edit_grades = False
        student.can_view_grades = False
        student.can_edit_assignment = False
        student.can_view_assignment = True
        student.can_submit_assignment = True
        student.save()

    def gen_random_participation_for_each_user(self):
        """Generate participants to link students to courses with a role."""
        courses = Course.objects.all()
        participation_list = list()
        if courses.count() > 0:
            for user in User.objects.all():
                participation = Participation()
                participation.user = user
                participation.course = courses[random.randint(0, len(courses) - 1)]
                participation.role = random.choice(Role.objects.all())
                try:
                    Participation.objects.get(course=participation.course, user=participation.user)
                except Exception:
                    participation_list.append(participation)

        # Using a bulk create speeds the process up.
        Participation.objects.bulk_create(participation_list)

    def gen_random_assignments(self, amount):
        """Generate random assignments."""
        for _ in range(amount):
            if Course.objects.all().count() == 0:
                continue
            format = JournalFormat()
            format.save()
            assignment = Assignment(format=format)
            assignment.save()
            assignment.name = faker.catch_phrase()
            assignment.deadline = faker.date_time_between(start_date="now", end_date="+1y", tzinfo=None)
            assignment.author = User.objects.get(pk=1)
            assignment.description = faker.paragraph()
            courses = Course.objects.all()
            course_list = list()
            for course in random.choices(courses, k=3):
                if assignment.courses.count():
                    course_list.append(course)
                else:
                    if random.randint(1, 101) > 70:
                        course_list.append(course)

            assignment.courses.add(*(course_list))
            assignment.save()

    def gen_random_journals(self):
        """Generate random journals."""
        for assignment in Assignment.objects.all():
            for user in User.objects.all():
                if Journal.objects.filter(assignment=assignment, user=user).count() > 0:
                    continue
                factory.make_journal(assignment, user)

    def handle(self, *args, **options):
        """Generate randomly created data to create a more real life example."""
        amount = 4
        # Random users
        self.gen_random_users(amount)
        # Random course
        self.gen_random_courses(amount * 10)
        # Create the roles
        self.gen_roles()
        # Random participation
        self.gen_random_participation_for_each_user()
        # Random assignments
        self.gen_random_assignments(amount)
        # Random journals
        self.gen_random_journals()
