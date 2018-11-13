"""
group utilities.

A library with utilities related to groups.
"""
import VLE.factory as factory
from VLE.models import Group


def get_and_init_group(name, course):
    """Get a group and creates it if it does not exists yet."""
    if name == '':
        return None

    try:
        group = Group.objects.get(name=name, course=course)
    except Group.DoesNotExist:
        group = factory.make_course_group(name=name, course=course)
    return group
