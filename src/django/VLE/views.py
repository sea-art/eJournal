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

    if not user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'courses': []}
    for course in user.participant.all():
        course_obj = {
            'name': str(course.name),
            'auth': str(course.authors),
            'date': str(course.startdate),
            'abbr': str(course.abbreviation),
            'cID': str(course.abbreviation)
        }
        response['courses'].append(course_obj)

    return JsonResponse(response)


@api_view(['GET'])
def test(request, format=None):
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    return JsonResponse({'result': 'success',
                         'user': request.user.username})
