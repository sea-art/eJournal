from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Participation
from VLE.models import Role
from django.forms.models import model_to_dict

import random


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
    permissions = get_permissions(user, cID)

    for permission in permissionList:
        if permissions[permission] is False:
            return False

    return True


def get_permissions(user, cID):
    """Get the permissions of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    # First get the role ID of the user participation.
    role = Participation.objects.get(user=user, course=cID).role

    roleDict = model_to_dict(role)

    return roleDict
