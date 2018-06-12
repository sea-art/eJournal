from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *


@api_view(['GET'])
def test(request, format=None):
    return JsonResponse({'result': 'success',
                         'user': request.user.username})


@api_view(['GET'])
def get_user_courses(request):
    user = request.user
    response = {'result': 'success', 'courses': []}

    if not user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    courses = user.participant.all()
    for course in courses:
        response['courses'].append(CourseSerializer(course).data)
    return JsonResponse(response)


@api_view(['GET'])
def get_journal(request):
    pass
