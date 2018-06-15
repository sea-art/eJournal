from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal


def make_user(username, password, email=None, lti_id=None):
    user = User(username=username)
    user.save()
    user.set_password(password)
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
