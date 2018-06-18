from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
import random


<<<<<<< HEAD
def make_user(username, password, email=None, lti_id=None):
=======
def make_user(username, password, profile_picture=None):
>>>>>>> 742e37dd714793d7a0aad514a7d688ab467c9de7
    user = User(username=username)
    user.save()
    user.set_password(password)
    user.profile_picture = profile_picture if profile_picture else '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_course(name, abbrev):
    course = Course(name=name, abbreviation=abbrev)
    course.save()
    return course


def make_assignment(name, description, author):
    assign = Assignment(name=name, description=description, author=author)
    assign.save()
    return assign


def make_journal(assignment, user):
    journal = Journal(assignment=assignment, user=user)
    journal.save()
    return journal
