"""
permissions.py.

All the permission functions.
"""
from VLE.models import Participation, Role

from django.forms.models import model_to_dict


def check_permissions(user, cID, permissionList):
    """Check if the user has the needed permissions.

    Check whether the user has the right permissions to access the given course functionality.
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
    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    return Role.objects.get(id=roleID)


def get_permissions(user, cID=-1):
    """Get permissions given a user.

    Get the permissions of the given user in the given course. The
    permissions are returned in dictionary format. For site-wide permissions
    when the user is not within a course, use cID == -1.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to retrieve the permissions. -1 for permissions
    outside of a course.
    """
    roleDict = {}

    if user.is_admin:
        # The call is made for system wide permissions and not course specific.
        # Administrators should not be able to view grades.
        roleDict = {
            "can_edit_grades": False,
            "can_view_grades": False,
            "can_edit_assignment": True,
            "can_view_assignment": True,
            "can_submit_assignment": True,
            "can_edit_course": True,
            "can_delete_course": True,
            "is_admin": True
        }
    elif cID is -1:
        # No course ID was given. The user has no permissions.
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
        # The course ID was given. Return the permissions of the user as dictionary.
        role = Participation.objects.get(user=user, course=cID).role

        roleDict = model_to_dict(role)
        roleDict['is_admin'] = False

    return roleDict
