"""
delete.py.

API functions that handle the delete requests.
"""
from rest_framework.decorators import api_view

from VLE.models import Assignment, Course, Participation, User

import VLE.views.responses as responses


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

    course = Course.objects.get(pk=request.data['cID'])
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
        user = User.objects.get(pk=request.data['uID'])
        course = Course.objects.get(pk=request.data['cID'])
        participation = Participation.objects.get(user=user, course=course)
    except (User.DoesNotExist, Course.DoesNotExist, Participation.DoesNotExist):
        return responses.not_found(description='User, Course or Participation does not exist.')

    participation.delete()

    return responses.success(message='Succesfully deleted student from course')
