"""
delete.py.

API functions that handle the delete requests.
"""
from rest_framework.decorators import api_view

from VLE.models import Assignment, Course, Participation, User

import VLE.views.responses as responses
import VLE.utils as utils
import VLE.permissions as permissions


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
