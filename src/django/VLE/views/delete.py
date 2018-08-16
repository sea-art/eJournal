"""
delete.py.

API functions that handle the delete requests.
"""
from rest_framework.decorators import api_view

from VLE.models import Assignment, Course, EntryComment, Participation, User, Role

import VLE.views.responses as responses
import VLE.utils.generic_utils as utils
import VLE.permissions as permissions


@api_view(['POST'])
def delete_course(request):
    """Delete an existing course.

    Arguments:
    request -- the update request that was send with
        cID -- course ID given with the request

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [cID] = utils.required_params(request.data, 'cID')
    except KeyError:
        return responses.keyerror('cID')

    # Courses can only be deleted with can_delete_course permission.
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.unauthorized(description="You have no access to this course")
    elif not role.can_delete_course:
        return responses.forbidden(description="You have no permissions to delete a course.")

    course = Course.objects.get(pk=cID)
    course.delete()

    return responses.success(message='Succesfully deleted course')


@api_view(['POST'])
def delete_assignment(request):
    """Delete an existing assignment from a course.

    If an assignment is not attached to any course it will be deleted.

    Arguments:
    request -- the update request that was send with
        aID -- assignment ID given with the request
        cID -- course ID given with the request

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        cID, aID = utils.required_params(request.data, 'cID', 'aID')
    except KeyError:
        return responses.keyerror('cID', 'aID')

    # Assignments can only be deleted with can_delete_assignment permission.
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.forbidden(description="You have no access to this course")
    elif not role.can_delete_assignment:
        return responses.forbidden(description="You have no permissions to delete a assignment.")

    response = {'removed_completely': False}
    course = Course.objects.get(pk=cID)
    assignment = Assignment.objects.get(pk=aID)
    assignment.courses.remove(course)
    assignment.save()
    response['removed_from_course'] = True
    if assignment.courses.count() == 0:
        assignment.delete()
        response['removed_completely'] = True

    return responses.success(message='Succesfully deleted assignment', payload=response)


@api_view(['POST'])
def delete_user_from_course(request):
    """Delete a student from course.

    Arguments:
    request -- the update request that was send with
        uID -- student ID given with the request
        cID -- course ID given with the request

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        uID, cID = utils.required_params(request.data, 'uID', 'cID')
    except KeyError:
        return responses.keyerror('uID', 'cID')

    # Users can only be deleted from the course with can_view_course_participants
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.unauthorized(description="You have no access to this course")
    elif not role.can_view_course_participants:
        return responses.forbidden(description="Uou have no permissions to delete this user.")

    try:
        user = User.objects.get(pk=uID)
        course = Course.objects.get(pk=cID)
        participation = Participation.objects.get(user=user, course=course)
    except (User.DoesNotExist, Course.DoesNotExist, Participation.DoesNotExist):
        return responses.not_found(description='User, Course or Participation does not exist.')

    participation.delete()
    return responses.success(message='Succesfully deleted student from course')


@api_view(['POST'])
def delete_course_role(request):
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        cID, name = utils.required_params(request.data, 'cID', 'name')
    except KeyError:
        return responses.keyerror('cID', 'name')

    # Users can only delete course roles with can_edit_course_roles
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.unauthorized(description="You have no access to this course")
    elif not role.can_edit_course_roles:
        return responses.forbidden(description="You have no permissions to delete this course role.")

    request_user_role = Participation.objects.get(user=request.user.id, course=cID).role

    if not request_user_role.can_edit_course_roles:
        return responses.forbidden()

    Role.objects.get(name=name, course=cID).delete()
    return responses.success(message='Succesfully deleted role from course')


@api_view(['POST'])
def delete_entrycomment(request):
    """Delete an entrycomment.

    Arguments:
    request -- the request that was send with
        ecID -- the entrycomment ID
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        ecID = utils.required_params(request.data, "ecID")[0]
    except KeyError:
        return responses.keyerror("ecID")

    try:
        entrycomment = EntryComment.objects.get(pk=ecID)
        entryAuthor = User.objects.get(pk=entrycomment.author.id)
    except (EntryComment.DoesNotExist, User.DoesNotExist):
        return responses.not_found('Comment or Author does not exist.')

    if not user == entryAuthor:
        return responses.forbidden()

    EntryComment.objects.get(id=ecID).delete()
    return responses.success(message='Succesfully deleted comment')
