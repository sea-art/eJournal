from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
import random


def make_user(username, password, profile_picture=None):
    user = User(username=username)
    user.save()
    user.set_password(password)
    if profile_picture:
        user.profile_picture = profile_picture
    else:
        user.profile_picture = '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_course(name, abbrev, startdate=None, author=None):
    course = Course.objects.create(
        name=name,
        abbreviation=abbrev,
        startdate=startdate,
        author=author
    )
    return course


def make_assignment(name, description, author=None):
    assign = Assignment.objects.create(
        name=name,
        description=description,
        author=author
    )
    return assign


def make_journal(assignment, user):
    journal = Journal.objects.create(
        assignment=assignment,
        user=user
    )
    return journal
