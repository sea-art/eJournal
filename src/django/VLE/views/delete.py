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

    return JsonResponse({'result': 'successfully deleted course'})


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
    print(assignment)
    assignment.delete()

    return JsonResponse({'result': 'successfully deleted assignemnt'})
