from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Participation
from VLE.models import Role


def hex_to_dec(hex):
    """Change hex string to int"""
    return int(hex, 16)


def dec_to_hex(dec):
    """Change int to hex value"""
    return hex(dec).split('x')[-1]


def check_permissions(user, cID, permissionList):
    """Check whether the user has the right permissions to access the given
    course functionality.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    role = get_role(user, cID)

    for permission in permissionList:
        if not getattr(role, permission):
            print("*Permission test message*: \tInsufficient user permissions!", permissionList)
            return False

    return True


def get_role(user, cID):
    """Get the role and permissions of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    role = Role.objects.get(id=roleID)

    return role


def make_user(username, password):
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
