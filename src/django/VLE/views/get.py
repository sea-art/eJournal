"""
get.py.

API functions that handle the get requests.
"""
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import redirect

import statistics as st
import json

import VLE.lti_launch as lti
import VLE.edag as edag
import VLE.utils as utils
from VLE.models import Assignment, Course, Participation, Journal, EntryTemplate, EntryComment, User, Node
import VLE.serializers as serialize
import VLE.permissions as permission
import VLE.views.responses as responses

# VUE ENTRY STATE
BAD_AUTH = '-1'
NO_COURSE = '0'
NO_ASSIGN = '1'
NEW_COURSE = '2'
NEW_ASSIGN = '3'
FINISH_T = '4'
FINISH_S = '5'
GRADE_CENTER = '6'


@api_view(['GET'])
def get_own_user_data(request):
    """Get the data linked to the logged in user.

    Arguments:
    request -- the request that was send with

    Returns a json string with user data
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    user_dict = serialize.user_to_dict(user)
    user_dict['grade_notifications'] = user.grade_notifications
    user_dict['comment_notifications'] = user.comment_notifications
    return responses.success(payload={'user': user_dict})


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
        return responses.unauthorized()

    course = serialize.course_to_dict(Course.objects.get(pk=cID))

    return responses.success(payload={'course': course})


@api_view(['GET'])
def get_course_users(request, cID):
    """Get all users for a given course, including their role for this course.

    Arguments:
    request -- the request
    cID -- the course ID

    Returns a json string with a list of participants.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    participations = course.participation_set.all()
    return responses.success(payload={'users': [serialize.participation_to_dict(participation)
                                                for participation in participations]})


@api_view(['GET'])
def get_unenrolled_users(request, cID):
    """Get all users not connected to a given course.

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
        return responses.not_found('Course does not exist.')

    ids_in_course = course.participation_set.all().values('user__id')
    result = User.objects.all().exclude(id__in=ids_in_course)

    return responses.success(payload={'users': [serialize.user_to_dict(user) for user in result]})


@api_view(['GET'])
def get_user_courses(request):
    """Get the courses that are linked to the user linked to the request.

    Arguments:
    request -- the request that was send with

    Returns a json string with the courses for the requested user
    """
    user = request.user

    if not user.is_authenticated:
        return responses.unauthorized()

    courses = []

    for course in user.participations.all():
        courses.append(serialize.course_to_dict(course))

    return response.success(payload={'courses': courses})


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

    return response.success(payload={'courses': courses})


def get_linkable_courses_user(user):
    """Get all courses that the current user is connected with as sufficiently
    authenticated user. The lti_id should be equal to NULL. A user can then link
    this course to Canvas.

    Arguments:
    user -- the user that requested the linkable courses.

    Returns all of the courses."""
    courses = []
    unlinked_courses = Course.objects.filter(participation__user=user.id,
                                             participation__role__can_edit_course=True, lti_id=None)

    for course in unlinked_courses:
        courses.append(serialize.course_to_dict(course))

    return courses


def get_teacher_course_assignments(user, course):
    """Get the assignments from the course ID with extra information for the teacher.

    Arguments:
    user -- user that requested the assignments, this is to validate the request
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    # TODO: check permission

    assignments = []
    for assignment in course.assignment_set.all():
        assignments.append(serialize.assignment_to_dict(assignment))

    return assignments


def get_student_course_assignments(user, course):
    """Get the assignments from the course ID with extra information for the student.

    Arguments:
    user -- user that requested the assignments, this is to validate the request
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    # TODO: check permission
    assignments = []
    for assignment in Assignment.objects.get_queryset().filter(courses=course, journal__user=user):
        assignments.append(serialize.student_assignment_to_dict(assignment, user))

    return assignments


@api_view(['GET'])
def get_course_assignments(request, cID):
    """Get the assignments from the course ID with extra information for the requested user.

    Arguments:
    request -- the request that was send with
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    course = Course.objects.get(pk=cID)
    participation = Participation.objects.get(user=user, course=course)

    # Check whether the user can edit the course.
    if participation.role.can_grade_journal:
        return responses.success(payload={'assignments': get_teacher_course_assignments(user, course)})
    else:
        return responses.success(payload={'assignments': get_student_course_assignments(user, course)})


@api_view(['GET'])
def get_assignment_data(request, cID, aID):
    """Get the data linked to an assignemnt ID.

    Arguments:
    request -- the request that was send with
    cID -- course ID given with the request
    aID -- assignemnt ID given with the request

    Returns a json string with the assignment data for the requested user.
    Depending on the permissions, return all student journals or a specific
    student's journal.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    course = Course.objects.get(pk=cID)
    assignment = Assignment.objects.get(pk=aID)
    participation = Participation.objects.get(user=user, course=course)

    if participation.role.can_grade_journal:
        return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})
    else:
        return responses.success(payload={'assignment': serialize.student_assignment_to_dict(assignment, request.user)})


@api_view(['GET'])
def get_assignment_journals(request, aID):
    """Get the student submitted journals of one assignment.

    Arguments:
    request -- the request that was send with
    cID -- the course ID to get the assignments from

    Returns a json string with the journals
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        assignment = Assignment.objects.get(pk=aID)
        # TODO: Not first, for demo.
        course = assignment.courses.first()
        participation = Participation.objects.get(user=user, course=course)
    except (Participation.DoesNotExist, Assignment.DoesNotExist):
        return responses.not_found('Assignment or Participation does not exist.')

    if not participation.role.can_view_assignment_participants:
        return responses.forbidden('You are not allowed to view assignment participants.')

    journals = []

    for journal in assignment.journal_set.all():
        journals.append(serialize.journal_to_dict(journal))

    stats = {}
    if journals:
        # TODO: Maybe make this efficient for minimal delay?
        stats['needsMarking'] = sum([x['stats']['submitted'] - x['stats']['graded'] for x in journals])
        points = [x['stats']['acquired_points'] for x in journals]
        stats['avgPoints'] = round(st.mean(points), 2)
        stats['medianPoints'] = st.median(points)
        stats['avgEntries'] = round(
            st.mean([x['stats']['total_points'] for x in journals]), 2)

    return responses.success(payload={'stats': stats if stats else None, 'journals': journals})


@api_view(['GET'])
def get_upcoming_deadlines(request):
    """Get upcoming deadlines for the requested user.

    Arguments:
    request -- the request that was send with

    Returns a json string with the deadlines
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    # TODO: Only take user specific upcoming enties
    deadlines = []
    for assign in Assignment.objects.all():
        deadlines.append(serialize.deadline_to_dict(assign))

    return responses.success(payload={'deadlines': deadlines})


@api_view(['GET'])
def get_course_permissions(request, cID):
    """Get the permissions of a course.

    Arguments:
    request -- the request that was sent
    cID     -- the course id (string)

    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    roleDict = permission.get_permissions(request.user, int(cID))

    return responses.success(payload={'permissions': roleDict})


@api_view(['GET'])
def get_nodes(request, jID):
    """Get all nodes contained within a journal.

    Arguments:
    request -- the request that was sent
    jID     -- the journal id

    Returns a json string containing all entry and deadline nodes.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    journal = Journal.objects.get(pk=jID)
    return responses.success(payload={'nodes': edag.get_nodes_dict(journal, request.user)})


@api_view(['GET'])
def get_format(request, aID):
    """Get the format attached to an assignment.

    Arguments:
    request -- the request that was sent
    aID     -- the assignment id

    Returns a json string containing the format.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment does not exist.')

    return responses.success(payload={'format': serialize.format_to_dict(assignment.format)})


@api_view(['GET'])
def get_template(request, tID):
    """Get a template.

    Arguments:
    request -- the request that was sent
    tID     -- the template id

    Returns a json string containing the format.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        template = EntryTemplate.objects.get(pk=tID)
    except EntryTemplate.DoesNotExist:
        return responses.not_found('Template does not exist.')

    return responses.success(payload={'template': serialize.template_to_dict(template)})


@api_view(['GET'])
def get_user_teacher_courses(request):
    """Get all the courses where the user is a teacher.

    Arguments:
    request -- the request that was sent

    Returns a json string containing the format.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    q_courses = Course.objects.filter(participation__user=request.user.id,
                                      participation__role__can_edit_course=True)
    courses = []
    for course in q_courses:
        courses.append(serialize.course_to_dict(course))
    return JsonResponse({'result': 'success', 'courses': courses}, status=200)


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
        return responses.unauthorized()

    cID, aID, jID, tID = utils.optional_params(request.data, "cID", "aID", "jID", "tID")
    result = {}

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
        return responses.not_found('Course, Assignment, Journal or Template does not exist.')

    return responses.success(payload=result)


@api_view(['GET'])
def get_entrycomments(request, entryID):
    """Get the comments belonging to the specified entry based on its entryID."""
    if not request.user.is_authenticated:
        return responses.unauthorized()

    entrycomments = EntryComment.objects.filter(entry=entryID)
    return responses.success(payload={
        'entrycomments': [serialize.entrycomment_to_dict(comment) for comment in entrycomments]
        })


@api_view(['GET'])
def get_user_data(request, uID):
    """Get the user data of the given user.

    Get his/her profile data and posted entries with the titles of the journals of the user based on the uID.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    user = User.objects.get(pk=uID)

    # Check the right permissions to get this users data, either be the user of the data or be an admin.
    permissions = permission.get_permissions(user, cID=-1)
    if not (permissions['is_admin'] or request.user.id == uID):
        return responses.forbidden('You cannot view this users data.')

    profile = serialize.user_to_dict(user)
    # Don't send the user id with it.
    del profile['uID']

    journals = Journal.objects.filter(user=uID)
    journal_dict = {}
    for journal in journals:
        # Select the nodes of this journal but only the ones with entries.
        nodes_of_journal_with_entries = Node.objects.filter(journal=journal).exclude(entry__isnull=True)
        # Serialize all entries and put them into the entries dictionary with the assignment name key.
        entries_of_journal = [serialize.export_entry_to_dict(node.entry) for node in nodes_of_journal_with_entries]
        journal_dict.update({journal.assignment.name: entries_of_journal})

    return responses.success(payload={'profile': profile, 'journals': journal_dict})


@api_view(['GET'])
def get_assignment_by_lti_id(request, lti_id):
    """Get an assignment if it exists.

    Arguments:
    request -- the request that was sent
    lti_id -- lti_id of the assignment
    """
    if not request.user.is_authenticated:
        return response.unauthorized()
    try:
        assignment = Assignment.objects.get(lti_id=lti_id)
        return response.succes(payload={'assignment': serialize.assignment_to_dict(assignment)})
    except Assignment.DoesNotExist:
        return response.no_content()


@api_view(['POST'])
def lti_launch(request):
    """Django view for the lti post request."""
    secret = settings.LTI_SECRET
    key = settings.LTI_KEY

    authenticated, err = lti.OAuthRequestValidater.check_signature(
        key, secret, request)

    if authenticated:
        # Select or create the user, course, assignment and journal.
        roles = json.load(open('config.json'))
        lti_roles = dict((roles[k], k) for k in roles)

        user = lti.select_create_user(request.POST, roles)
        role = lti_roles[request.POST['roles']]

        token = TokenObtainPairSerializer.get_token(user)
        access = token.access_token

        course_names = ['lti_cName', 'lti_abbr', 'lti_cID']
        course_values = [request.POST['context_title'],
                         request.POST['context_label'],
                         request.POST['context_id']]
        assignment_names = ['lti_aName', 'lti_aID']
        assignment_values = [request.POST['resource_link_title'],
                             request.POST['resource_link_id']]
        if 'custom_canvas_assignment_points_possible' in request.POST:
            assignment_names.append('lti_points_possible')
            assignment_values.append(
                request.POST['custom_canvas_assignment_points_possible'])

        course = lti.check_course_lti(request.POST, user, lti_roles[
            request.POST['roles']])
        if course is None:
            if role == 'Teacher':
                q_names = ['jwt_refresh', 'jwt_access', 'state']
                q_names += course_names
                q_names += assignment_names
                q_values = [token, access, NEW_COURSE]
                q_values += course_values
                q_values += assignment_values
                return redirect(lti.create_lti_query_link(q_names, q_values))
            else:
                q_names = ['jwt_refresh', 'jwt_access', 'state']
                q_values = [token, access, NO_COURSE]
                return redirect(lti.create_lti_query_link(q_names, q_values))

        assignment = lti.check_assignment_lti(request.POST)
        if assignment is None:
            if role == 'Teacher':
                q_names = ['jwt_refresh', 'jwt_access', 'state', 'cID']
                q_names += assignment_names
                q_values = [token, access, NEW_ASSIGN, course.pk]
                q_values += assignment_values
                return redirect(lti.create_lti_query_link(q_names, q_values))
            else:
                q_names = ['jwt_refresh', 'jwt_access', 'state']
                q_values = [token, access, NO_ASSIGN]
                return redirect(lti.create_lti_query_link(q_names, q_values))

        journal = lti.select_create_journal(request.POST, user, assignment, roles)
        jID = journal.pk if journal is not None else None
        state = FINISH_T if jID is None else FINISH_S

        q_names = ['jwt_refresh', 'jwt_access',
                   'state', 'cID', 'aID', 'jID']
        q_values = [token, access, state,
                    course.pk, assignment.pk, jID]
        return redirect(lti.create_lti_query_link(q_names, q_values))

    return redirect(lti.create_lti_query_link(['state'], ['BAD_AUTH']))
