from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *
from random import randint
from VLE.util import *


def user_to_obj(user):
    """Get a object of a single user

    Arguments:
    user -- user to create the object with

    returns object of that user
    """
    return {
        'name': str(user),
        'picture': user.profile_picture if user.profile_picture else '../assets/logo.png',
        'uID': dec_to_hex(user.id)
    } if user else None


@api_view(['GET'])
def get_user_courses(request):
    """Get the courses that are linked to the user linked to the request

    Arguments:
    request -- the request that was send with

    Returns a json string with the courses for the requested user
    """
    user = request.user

    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    courses = []
    for course in user.participations.all():
        courses.append({
            'cID': dec_to_hex(course.id),
            'name': str(course),
            'auth': user_to_obj(course.author),
            'date': course.startdate,
            'abbr': course.abbreviation
        })

    return JsonResponse({'result': 'success', 'courses': courses})


def get_teacher_course_assignments(user, course):
    """Get the assignments from the course ID with extra information for the teacher

    Arguments:
    user -- user that requested the assignments, this is to validate the request
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    # TODO: check permission

    assignments = []
    for assignment in course.assignment_set.all():
        assignments.append({
            'aID': dec_to_hex(assignment.id),
            'name': str(assignment),
            'auth': user_to_obj(assignment.author),
            'description': assignment.description,
            'progress': {'acquired': randint(0, 10), 'total': 10}  # TODO: Change random to real progress
        })

    return assignments


def get_student_course_assignments(user, course):
    """Get the assignments from the course ID with extra information for the student

    Arguments:
    user -- user that requested the assignments, this is to validate the request
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    # TODO: check permission
    assignments = []
    for assignment in Assignment.objects.get_queryset().filter(courses=course):
        try:
            journal = Journal.objects.get(assignment=assignment, user=user)
        except Journal.DoesNotExist:
            continue

        assignments.append({
            'aID': dec_to_hex(assignment.pk),
            'name': assignment.name,
            'progress': {'acquired': randint(0, 10), 'total': 10},  # TODO: Change random to real progress
            'stats': {'graded': 1, 'total': 1},
            'description': str(assignment.description),
            'jID': dec_to_hex(journal.id)
        })

    return assignments


@api_view(['GET'])
def get_course_assignments(request, cID):
    """Get the assignments from the course ID with extra information for the requested user

    Arguments:
    request -- the request that was send with
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = Course.objects.get(pk=hex_to_dec(cID))
    participation = Participation.objects.get(user=user, course=course)

    if participation.role.can_view_assignment:
        return JsonResponse({
            'result': 'success',
            'assignments': get_teacher_course_assignments(user, course)
        })
    else:
        return JsonResponse({
            'result': 'success',
            'assignments': get_student_course_assignments(user, course)
        })


@api_view(['GET'])
def get_assignment_journals(request, aID):
    """Get the student submitted journals of one assignment

    Arguments:
    request -- the request that was send with
    cID -- the course ID to get the assignments from

    Returns a json string with the journals
    """
    user = request.user
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    # TODO: Check if the user has valid permissions to see get all the journals (teacher/ta)
    assignment = Assignment.objects.get(pk=hex_to_dec(aID))
    journals = []

    for journal in assignment.journal_set.all():
        journals.append({
            'jID': dec_to_hex(journal.id),
            'student': user_to_obj(journal.user),
            'progress': {'acquired': randint(0, 5), 'total': randint(5, 10)},  # TODO: Add real progress
            'stats': {'graded': randint(0, 5), 'total': randint(5, 10)},  # TODO: Add real stats
        })

    # TODO: Misschien dit efficient maken voor minimal delay?
    needsMarking = sum([x.get("stats").get("total") - x.get("stats").get("graded") for x in journals])
    points = [x.get("progress").get("acquired") for x in journals]
    avgPoints = round(st.mean(points), 2)
    medianPoints = st.median(points)
    avgEntries = round(st.mean([x.get("stats").get("total") for x in journals]), 2)

    stats = {
        'needsMarking': needsMarking,
        'avgPoints': avgPoints,
        'medianPoints': medianPoints,
        'avgEntries': avgEntries
    }

    return JsonResponse({'result': 'success', 'stats': stats, 'journals': journals})


@api_view(['GET'])
def get_upcoming_deadlines(request):
    """Get upcoming deadlines for the requested user.

    Arguments:
    request -- the request that was send with

    Returns a json string with the deadlines
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    # TODO: Only take user specific upcoming enties
    deadlines = []
    for assign in Assignment.objects.all():
        deadlines.append({
            'dID': dec_to_hex(assign.id),
            'name': assign.name,
            'course': [c.abbreviation for c in assign.courses.all()],
            'datetime': assign.deadline,
            'cID': [dec_to_hex(c.id) for c in assign.courses.all()]
        })

    return JsonResponse({'result': 'success', 'deadlines': deadlines})


@api_view(['GET'])
def get_course_permissions(request, cID):
    """TODO"""
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    roleDict = vars(get_role(request.user, cID))

    return JsonResponse({'permissions': roleDict})
