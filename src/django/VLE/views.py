from rest_framework.decorators import api_view
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from VLE.serializers import *
from random import randint


def hex_to_dec(hex):
    """Change hex string to int"""
    return int(hex, 16)


def dec_to_hex(dec):
    """Change int to hex value"""
    return hex(dec).split('x')[-1]


def check_permissions(user, cID, permissionList):
    """Check whether the user has the right permissions to access the given
    course functionality.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    role = get_role(user, cID)

    for permission in permissionList:
        if not getattr(role, permission):
            print("*Permission test message*: \tInsufficient user permissions!", permissionList)
            return False

    return True


def get_role(user, cID):
    """Get the role and permissions of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    role = Role.objects.get(id=roleID)

    return role


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
            'name': str(course),
            'auth': str(course.author),
            'date': course.startdate,
            'abbr': course.abbreviation,
            'cID': dec_to_hex(course.id)
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
            'auth': str(assignment.author),
            'description': str(assignment.description),
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
            'student': str(journal.user),
            'studentnumber': journal.user.id,
            'progress': {'acquired': str(10), 'total': str(10)},
            'studentPortraitPath': str('../assets/logo.png'),
            'entryStats': {'graded': 1, 'total': 1},  # TODO: Add real stats
            'uID': dec_to_hex(journal.id)
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
            'name': assign.name,
            'course': [c.abbreviation for c in assign.courses.all()],
            'cID': [dec_to_hex(c.id) for c in assign.courses.all()],
            'dID': dec_to_hex(assign.id),
            'datetime': assign.deadline
        })

    return JsonResponse({'result': 'success', 'deadlines': deadlines})
