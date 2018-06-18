from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *
from VLE.util import make_course
from random import randint


def user_to_obj(user):
    """Get a object of a single user

    Arguments:
    user -- user to create the object with

    returns object of that user
    """
    return {
        'name': str(user),
        'picture': user.profile_picture if user.profile_picture else '../assets/logo.png',
        'uID': user.id
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
            'cID': course.id,
            'name': str(course),
            'auth': user_to_obj(course.author),
            'date': course.startdate,
            'abbr': course.abbreviation
        })

    for course in Course.objects.all().filter(author=user):
        courses.append({
            'cID': course.id,
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
            'aID': assignment.id,
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
            'aID': assignment.pk,
            'name': assignment.name,
            'progress': {'acquired': randint(0, 10), 'total': 10},  # TODO: Change random to real progress
            'stats': {'graded': 1, 'total': 1},
            'description': str(assignment.description),
            'jID': journal.id
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

    course = Course.objects.get(pk=cID)
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
    assignment = Assignment.objects.get(pk=aID)
    journals = []
    for journal in assignment.journal_set.all():
        journals.append({
            'jID': journal.id,
            'student': user_to_obj(journal.user),
            'progress': {'acquired': 10, 'total': 10},  # TODO: Add real progress
            'stats': {'graded': 1, 'total': 1},  # TODO: Add real stats
        })

    return JsonResponse({'result': 'success', 'journals': journals})


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
            'dID': assign.id,
            'name': assign.name,
            'course': [c.abbreviation for c in assign.courses.all()],
            'datetime': assign.deadline,
            'cID': [c.id for c in assign.courses.all()]
        })

    return JsonResponse({'result': 'success', 'deadlines': deadlines})


@api_view(['POST'])
def create_new_course(request):
    """Create a new course

    Arguments:
    request -- the request that was send with
    name -- name of the course
    abbr -- abbreviation of the course
    startdate -- date when the course starts

    Returns a json string for if it is succesful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = make_course(request.data["name"], request.data["abbr"], request.data["startdate"], request.user)

    return JsonResponse({'result': 'success', 'course': {
        'cID': course.id,
        'name': str(course),
        'auth': user_to_obj(course.author),
        'date': course.startdate,
        'abbr': course.abbreviation
    }}, status=200)
