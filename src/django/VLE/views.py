from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *


def hex_to_dec(hex):
    return int(hex, 16)


def dec_to_hex(dec):
    return hex(dec).split('x')[-1]


@api_view(['GET'])
def get_user_courses(request):
    """
    Returns the courses for an user.
    """
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'courses': []}
    for course in user.participations.all():
        course_obj = {
            'name': str(course.name),
            'auth': str(course.author),
            'date': str(course.startdate),
            'abbr': str(course.abbreviation),
            'cID': str(dec_to_hex(course.id))
        }
        response['courses'].append(course_obj)
    return JsonResponse(response)


@api_view(['GET'])
def get_course_assignments(request, cID):
    """
    Get the participants of a course.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'assignments': []}
    # TODO: check permission
    course = Course.objects.get(pk=hex_to_dec(cID))
    for assignment in course.assignment_set.all():
        assignment_obj = {
            'name': str(assignment.name),
            'auth': str(assignment.author),
            'progress': str(0),
        }
        response['assignments'].append(assignment_obj)
    return JsonResponse(response)


@api_view(['GET'])
def get_assignment_journals(request, aID):
    """
    Get the journals of one assignment.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': '401 Authentication Error'}, status=401)

    response = {'result': 'success', 'journals': []}
    # TODO: check permission
    assignment = Assignment.objects.get(pk=hex_to_dec(aID))
    for journal in assignment.journal_set.all():
        journal_obj = {
            'student': str(journal.user.username),
            'studentnumber': str("00000000"),
            'progress': {'acquired': str(10), 'total': str(10)},
            'studentPortraitPath': str('../assets/logo.png'),
            'entrieStats': {'graded': 1, 'total': 1},
            'uid': dec_to_hex(journal.id)
        }
        response['journals'].append(journal_obj)
    return JsonResponse(response)
