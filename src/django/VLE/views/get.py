from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.shortcuts import redirect
import statistics as st
import json
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

import VLE.factory as factory
import VLE.edag as edag
import VLE.utils as utils
from VLE.serializers import *
from VLE.permissions import *
from VLE.lti_launch import OAuthRequestValidater, select_create_user, \
    create_lti_query_link, check_course_lti, check_assignment_lti, \
    select_create_journal
from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import Journal


NEW_COURSE = 0
NEW_ASSIGNMENT = 1
FINISH_TEACHER = 2
FINISH_STUDENT = 3


@api_view(['GET'])
def get_own_user_data(request):
    """
    Get the data linked to the logged in user.

    Arguments:
    request -- the request that was send with

    Returns a json string with user data
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    user_dict = user_to_dict(user)
    user_dict['grade_notifications'] = user.grade_notifications
    user_dict['comment_notifications'] = user.comment_notifications
    return JsonResponse({'result': 'success', 'user': user_dict})


@api_view(['GET'])
def get_course_data(request, cID):
    """Get the data linked to a course ID.

    Arguments:
    request -- the request that was send with
    cID -- course ID given with the request

    Returns a json string with the course data for the requested user
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = course_to_dict(Course.objects.get(pk=cID))

    return JsonResponse({'result': 'success', 'course': course})


@api_view(['GET'])
def get_course_users(request, cID):
    """Get all users for a given course, including their
    role for this course.

    Arguments:
    request -- the request
    cID -- the course ID

    Returns a json string with a list of participants.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Course does not exist.'}, status=404)

    participations = course.participation_set.all()
    return JsonResponse({'result': 'success',
                         'users': [participation_to_dict(participation)
                                   for participation in participations]})


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
        courses.append(course_to_dict(course))

    return JsonResponse({'result': 'success', 'courses': courses})


def get_linkable_courses(request):
    """Get all courses that the current user is connected with as sufficiently
    authenticated user. The lti_id should be equal to NULL. A user can then link
    this course to Canvas.

    Arguments:
    request -- contains the user that requested the linkable courses

    Returns all of the courses."""
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    courses = get_linkable_courses_user(user)

    return JsonResponse({'result': 'success', 'courses': courses})


def get_linkable_courses_user(user):
    """Get all courses that the current user is connected with as sufficiently
    authenticated user. The lti_id should be equal to NULL. A user can then link
    this course to Canvas.

    Arguments:
    user -- the user that requested the linkable courses.

    Returns all of the courses."""
    courses = []
    addedCourses = []
    participations = Participation.objects.filter(user=user.pk)

    for participation in participations:
        if participation.role.can_edit_course:
            course = participation.course

            if course.pk not in addedCourses:
                # Add all courses which the teacher can edit.
                courses.append(course_to_dict(course))
                addedCourses.append(course.pk)

    return courses


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
        assignments.append(assignment_to_dict(assignment))

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
    for assignment in Assignment.objects.get_queryset().filter(courses=course, journal__user=user):
        assignments.append(student_assignment_to_dict(assignment, user))

    return assignments


@api_view(['GET'])
def get_course_assignments(request, cID):
    """Get the assignments from the course ID with extra information for the
    requested user.

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
def get_assignment_data(request, cID, aID):
    """Get the data linked to an assignemnt ID

    Arguments:
    request -- the request that was send with
    cID -- course ID given with the request
    aID -- assignemnt ID given with the request

    Returns a json string with the assignemnt data for the requested user
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = Course.objects.get(pk=cID)
    assignment = Assignment.objects.get(pk=aID)
    participation = Participation.objects.get(user=user, course=course)

    if participation.role.can_view_assignment:
        return JsonResponse({
            'result': 'success',
            'assignment': assignment_to_dict(assignment)
        })
    else:
        return JsonResponse({
            'result': 'success',
            'assignment': student_assignment_to_dict(assignment, request.user)
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

    try:
        assignment = Assignment.objects.get(pk=aID)
        # TODO: Not first, for demo.
        course = assignment.courses.first()
        participation = Participation.objects.get(user=request.user, course=course)
    except (Participation.DoesNotExist, Assignment.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Assignment or Participation does not exist.'}, status=404)

    if not participation.role.can_view_assignment:
        return JsonResponse({'result': '403 Forbidden'}, status=403)

    journals = []

    for journal in assignment.journal_set.all():
        journals.append(journal_to_dict(journal))

    stats = {}
    if journals:
        # TODO: Misschien dit efficient maken voor minimal delay?
        stats['needsMarking'] = sum(
            [x['stats']['submitted'] - x['stats']['graded'] for x in journals])
        points = [x['stats']['acquired_points'] for x in journals]
        stats['avgPoints'] = round(st.mean(points), 2)
        stats['medianPoints'] = st.median(points)
        stats['avgEntries'] = round(
            st.mean([x['stats']['total_points'] for x in journals]), 2)

    return JsonResponse({'result': 'success', 'stats': stats if stats else None, 'journals': journals})


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
        deadlines.append(deadline_to_dict(assignment))

    return JsonResponse({'result': 'success', 'deadlines': deadlines})


@api_view(['GET'])
def get_course_permissions(request, cID):
    """Get the permissions of a course.
    Arguments:
    request -- the request that was sent
    cID     -- the course id (string)

    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    roleDict = get_permissions(request.user, int(cID))

    return JsonResponse({'result': 'success',
                         'permissions': roleDict})


@api_view(['GET'])
def get_nodes(request, jID):
    """Get all nodes contained within a journal.
    Arguments:
    request -- the request that was sent
    jID     -- the journal id

    Returns a json string containing all entry and deadline nodes.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    journal = Journal.objects.get(pk=jID)
    return JsonResponse({'result': 'success',
                         'nodes': edag.get_nodes_dict(journal)})


@api_view(['GET'])
def get_format(request, aID):
    """Get the format attached to an assignment.

    Arguments:
    request -- the request that was sent
    aID     -- the assignment id

    Returns a json string containing the format.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Assignment does not exist.'}, status=404)

    return JsonResponse({'result': 'success',
                         'nodes': get_format_dict(assignment.format)})


@api_view(['POST'])
def get_names(request):
    """Get the format attached to an assignment.

    Arguments:
    request -- the request that was sent
    cID -- optionally the course id
    aID -- optionally the assignment id
    jID -- optionally the journal id
    tID -- optionally the template id

    Returns a json string containing the names of the set fields.
    cID populates 'course', aID populates 'assignment', tID populates
    'template' and jID populates 'journal' with the users' name.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    cID, aID, jID, tID = utils.get_optional_post_params(request.data, "cID", "aID", "jID", "tID")
    result = JsonResponse({'result': 'success'})

    try:
        if cID:
            course = Course.objects.get(pk=cID)
            result.course = course.name
        if aID:
            assignment = Assignment.objects.get(pk=aID)
            result.assignment = assignment.name
        if jID:
            journal = Journal.objects.get(pk=jID)
            result.journal = journal.user.name
        if tID:
            template = EntryTemplate.objects.get(pk=tID)
            result.template = template.name

    except (Course.DoesNotExist, Assignment.DoesNotExist, Journal.DoesNotExist, EntryTemplate.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Course, Assignment, Journal or Template does not exist.'}, status=404)

    return result


@api_view(['POST'])
def get_entrycomments(request):
    """
    Get the comments belonging to the specified entry based on its entryID.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        entryID = utils.get_required_post_params(request.data, "entryID")
    except KeyError:
        return utils.keyerror_json("entryID")

    entrycomments = EntryComment.objects.filter(entry=entryID)
    return JsonResponse({'result': 'success',
                         'entrycomments': [entrycomment_to_dict(comment) for comment in entrycomments]})


@api_view(['POST'])
def lti_grade_replace_result(request):
    # TODO Extend the docstring with what is important in the request variable.
    """
    Replace a grade on the LTI instance based on the request.
    """

    secret = settings.LTI_SECRET
    key = settings.LTI_KEY

    grade_request = GradePassBackRequest(key, secret, None)
    grade_request.score = '0.5'
    grade_request.sourcedId = request.POST['lis_result_sourcedid']
    grade_request.url = request.POST['lis_outcome_service_url']
    response = grade_request.send_post_request()

    return JsonResponse(response)


@api_view(['POST'])
def lti_launch(request):
    """Django view for the lti post request."""
    secret = settings.LTI_SECRET
    key = settings.LTI_KEY

    authenticated, err = OAuthRequestValidater.check_signature(
        key, secret, request)

    if authenticated:
        # Select or create the user, course, assignment and journal.
        roles = json.load(open('config.json'))
        lti_roles = dict((roles[k], k) for k in roles)

        user = select_create_user(request.POST)

        token = TokenObtainPairSerializer.get_token(user)
        access = token.access_token

        course_names = ['lti_cName', 'lti_abbr', 'role', 'lti_cID']
        course_values = [request.POST['context_title'],
                         request.POST['context_label'],
                         lti_roles[request.POST['roles']],
                         request.POST['context_id']]
        assignment_names = ['lti_aName', 'lti_aID', 'lti_points_possible']
        assignment_values = [request.POST['resource_link_title'],
                             request.POST['resource_link_id'],
                             request.POST[
                                'custom_canvas_assignment_points_possible']]

        course = check_course_lti(request.POST, user, lti_roles[request.POST[
                                                                    'roles']])
        if course is None:
            query_names = ['jwt_refresh', 'jwt_access', 'state']
            query_names += course_names
            query_names += assignment_names
            query_values = [token, access, NEW_COURSE]
            query_values += course_values
            query_values += assignment_values
            return redirect(create_lti_query_link(query_names, query_values))

        assignment = check_assignment_lti(request.POST, user)
        if assignment is None:
            query_names = ['jwt_refresh', 'jwt_access', 'state', 'cID']
            query_names += assignment_names
            query_values = [token, access, NEW_ASSIGNMENT, course.pk]
            query_values += assignment_values
            return redirect(create_lti_query_link(query_names, query_values))

        journal = select_create_journal(request.POST, user, assignment, roles)
        jID = journal.pk if journal is not None else None
        query_names = ['jwt_refresh', 'jwt_access',
                       'state', 'cID', 'aID', 'jID']
        query_values = [token, access,
                        FINISH_TEACHER if jID is None else FINISH_STUDENT,
                        course.pk, assignment.pk, jID]
        return redirect(create_lti_query_link(query_names, query_values))

    return redirect(settings.BASELINK + '/ErrorPage')
    # return redirect(401_site) not 404
