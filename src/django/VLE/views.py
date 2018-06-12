from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *


@api_view(['GET'])
def get_user_courses(request):
    """
    Returns the courses for an user.
    """
    user = request.user
    response = {'result': 'success', 'courses': []}
    if user.is_authenticated:
        for course in user.participant.all():
            response['courses'].append(CourseSerializer(course).data)
        return JsonResponse(response)
    else:
        return JsonResponse({'result': 'fail', 'courses': ''})


@api_view(['GET'])
def get_journal(request):
    pass
