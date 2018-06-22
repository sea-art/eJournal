from rest_framework.decorators import api_view
from django.http import JsonResponse

from VLE.serializers import *
import VLE.factory as factory
from VLE.views.get import get_own_user_data


@api_view(['POST'])
def delete_course(request):
    """Deletes an existing course.

    Arguments:
    request -- the update request that was send with
        cID -- course ID given with the request

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = Course.objects.get(pk=request.data['cID'])
    course.delete()

    return JsonResponse({'result': 'Succesfully deleted course'}, status=202)


@api_view(['POST'])
def delete_assignment(request):
    """Deletes an existing assignment.

    Arguments:
    request -- the update request that was send with
        aID -- assignment ID given with the request

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    assignment = Assignment.objects.get(pk=request.data['aID'])
    assignment.delete()

    return JsonResponse({'result': 'Succesfully deleted assignment'}, status=202)


@api_view(['POST'])
def delete_user_from_course(request):
    """Deletes a student from course.

    Arguments:
    request -- the update request that was send with
        uID -- student ID given with the request
        cID -- course ID given with the request

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        user = User.objects.get(pk=request.data['uID'])
        course = Course.objects.get(pk=request.data['cID'])
        participation = Participation.objects.get(user=user, course=course)
    except (User.DoesNotExist, Course.DoesNotExist, Participation.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'User, Course or Participation does not exist.'}, status=404)

    participation.delete()
    return JsonResponse({'result': 'Succesfully deleted student from course'}, status=202)
