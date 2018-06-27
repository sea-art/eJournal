"""
delete.py.

API functions that handle the delete requests.
"""
from rest_framework.decorators import api_view

from VLE.models import Assignment, Course, Participation, User, Role

import VLE.views.responses as responses
import VLE.utils as utils


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

    cID = request.data['cID']

    participation = Participation.objects.get(user=user, course=cID)
    if participation is None:
        return responses.unauthorized()

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
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        cID, aID = utils.required_params(request.data, 'cID', 'aID')
    except KeyError:
        return responses.keyerror('cID', 'aID')

    response = {'removed_completely': False}
    course = Course.objects.get(pk=request.data['cID'])
    assignment = Assignment.objects.get(pk=request.data['aID'])
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
    if not request.user.is_authenticated:
        return responses.unauthorized()

    request_user_role = Participation.objects.get(user=request.user.id, course=request.data['cID']).role

    if not request_user_role.can_edit_course_roles:
        return responses.forbidden()

    Role.objects.get(name=request.data['name'], course=request.data['cID']).delete()
    return responses.success(message='Succesfully deleted role from course')
