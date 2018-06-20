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
    cID -- course ID used to validate the request. (string)
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
    cID -- course ID used to validate the request. (string)
    """
    cID = int(cID)

    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    role = Role.objects.get(id=roleID)

    return role


def get_permissions(user, cID):
    """Get the permissions of the given user in the given course. The
    permissions are returned in dictionary format.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request. (string)
    """
    cID = int(cID)

    roleDict = {}

    if user.is_admin:
        # The call is made for system wide permissions and not course specific.
        roleDict = {
            "can_edit_grades": True,
            "can_view_grades": True,
            "can_edit_assignment": True,
            "can_view_assignment": True,
            "can_submit_assignment": True,
            "can_edit_course": True,
            "can_delete_course": True,
            "is_admin": True
        }
    elif cID == -1:
        roleDict = {
            "can_edit_grades": False,
            "can_view_grades": False,
            "can_edit_assignment": False,
            "can_view_assignment": False,
            "can_submit_assignment": False,
            "can_edit_course": False,
            "can_delete_course": False,
            "is_admin": False
        }
    else:
        # First get the role ID of the user participation.
        role = Participation.objects.get(user=user, course=cID).role

        roleDict = model_to_dict(role)
        roleDict['is_admin'] = False

    return roleDict
