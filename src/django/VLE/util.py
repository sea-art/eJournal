from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Participation
from VLE.models import Role
from django.forms.models import model_to_dict

import random


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
            return False

    return True


def get_role(user, cID):
    """Get the role (with permissions) of the given user in the given course.

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


def get_permissions(user, cID):
    """Get the permissions of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    if user.is_admin:
        # The call is made for system wide permissions and not course specific.
        role = {
            can_edit_grades: True,
            can_view_grades: True,
            can_edit_assignment: True,
            can_view_assignment: True,
            can_submit_assignment: True,
            can_edit_course: True,
            can_delete_course: True,
            is_admin: True
        }
    else:
        # First get the role ID of the user participation.
        role = Participation.objects.get(user=user, course=cID).role

        roleDict = model_to_dict(role)
        roleDict['is_admin'] = False

    return roleDict


def is_admin(user):
    """Check whether the user is an administrator.

    Arguments:
    user -- user that did the request.
    """
    assert not(user is None)

    is_admin = User.objects.get(user=user).is_admin

    return is_admin
