"""
get.py.

API functions that handle the get requests.
"""
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import redirect

import statistics as st
import json

import VLE.lti_launch as lti
import VLE.edag as edag
import VLE.utils as utils
from VLE.models import Assignment, Course, Journal, EntryTemplate, EntryComment, User, Node, \
    Role, Entry
import VLE.serializers as serialize
import VLE.permissions as permissions
import VLE.views.responses as responses

from datetime import datetime

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

    try:
        q_course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    if not permissions.is_user_in_course(user, q_course):
        return responses.forbidden('You are not in this course.')

    course = serialize.course_to_dict(q_course)

    return responses.success(payload={'course': course})


@api_view(['GET'])
def get_course_users(request, cID):
    """Get all users for a given course, including their role for this course.

    Arguments:
    request -- the request
    cID -- the course ID

    Returns a json string with a list of participants.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_view_course_participants:
        return responses.forbidden('You cannot view participants in this course.')

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
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_view_course_participants:
        return responses.forbidden('You cannot view participants in this course.')

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
    return responses.success(payload={'courses': courses})


@api_view(['GET'])
def get_linkable_courses(request):
    """Get linkable courses.

    Get all courses that the current user is connected with as sufficiently
    authenticated user. The lti_id should be equal to NULL. A user can then link
    this course to Canvas.

    Arguments:
    request -- contains the user that requested the linkable courses

    Returns all of the courses.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    if not user.is_teacher:
        return responses.forbidden("You are not allowed to add courses.")

    courses = []
    unlinked_courses = Course.objects.filter(participation__user=user.id,
                                             participation__role__can_edit_course=True, lti_id=None)

    for course in unlinked_courses:
        courses.append(serialize.course_to_dict(course))

    return responses.success(payload={'courses': courses})


def get_teacher_course_assignments(user, course):
    """Get the assignments from the course ID with extra information for the teacher.

    Arguments:
    user -- user that requested the assignments, this is to validate the request
    cID -- the course ID to get the assignments from

    Returns a json string with the assignments for the requested user
    """
    # TODO: Extra information for the teacher.

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
    assignments = []
    for assignment in Assignment.objects.filter(courses=course, journal__user=user):
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

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')

    # Check whether the user can grade a journal in the course.
    if role.can_grade_journal:
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

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment does not exist.')

    if role.can_grade_journal:
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
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment does not exist.')

    if not permissions.has_assignment_permission(user, assignment, 'can_view_assignment_participants'):
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
            st.mean([x['stats']['submitted'] for x in journals]), 2)

    return responses.success(payload={'stats': stats if stats else None, 'journals': journals})


def create_teacher_assignment_deadline(course, assignment):
    """Creates and returns the earliest deadline with data of an assignment
       from a teacher.

    Arguments:
    coures -- the course save information in the dictionary
    cID -- the assignment to get the deadlines

    Returns a dictionary with information of the assignment deadline.
    """
    journals = []

    for journal in assignment.journal_set.all():
        journals.append(serialize.journal_to_dict(journal))

    totalNeedsMarking = sum([x['stats']['submitted'] - x['stats']['graded'] for x in journals])

    format = serialize.format_to_dict(assignment.format)
    print(len(format['presets']))
    if len(format['presets']) == 0:
        return {}

    deadline_data = format['presets'][0]['deadline']
    splitted_deadline = deadline_data.split(' ')
    deadline = [splitted_deadline[0],
                splitted_deadline[1].split(':')[0],
                splitted_deadline[1].split(':')[1]]
    deadline = {'Date': deadline[0],
                'Hours': deadline[1],
                'Minutes': deadline[2]
                }

    return {'name': serialize.assignment_to_dict(assignment)['name'],
            'courseAbbr': course.abbreviation,
            'cID': course.id,
            'aID': assignment.id,
            'jID': journal.id,
            'deadline': deadline,
            'totalNeedsMarking': totalNeedsMarking}


def create_student_assignment_deadline(user, course, assignment):
    """Creates and returns the earliest deadline with data of an assignment
       from a student.

    Arguments:
    coures -- the course save information in the dictionary
    cID -- the assignment to get the deadlines

    Returns a dictionary with information of the assignment deadline.
    """
    try:
        journal = Journal.objects.get(assignment=assignment, user=user)
    except Journal.DoesNotExist:
        return {}

    deadlines = journal.node_set.exclude(preset=None).values('preset__deadline')
    if len(deadlines) == 0:
        return {}

    # Gets the node with the earliest deadline
    future_deadline = deadlines.filter(preset__deadline__gte=datetime.now()).order_by('preset__deadline')[0]
    future_deadline = {'Date': future_deadline['preset__deadline'].date(),
                       'Hours': future_deadline['preset__deadline'].hour,
                       'Minutes': future_deadline['preset__deadline'].minute}

    return {'name': serialize.assignment_to_dict(assignment)['name'],
            'courseAbbr': course.abbreviation,
            'cID': course.id,
            'aID': assignment.id,
            'jID': journal.id,
            'deadline': future_deadline,
            'totalNeedsMarking': 0}


@api_view(['GET'])
def get_upcoming_deadlines(request):
    """Get upcoming deadlines for the requested user.

    Arguments:
    request -- the request that was send with

    Returns a json string with the deadlines
    """

    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    courses = []
    deadline_list = []

    for course in user.participations.all():
        courses.append(course)

    for course in courses:
        role = permissions.get_role(user, course)

        if role is None:
            return responses.forbidden('You are not in this course.')

        if role.can_grade_journal:
            for assignment in Assignment.objects.filter(courses=course.id, journal__user=user).all():
                deadline = create_teacher_assignment_deadline(course, assignment)
                if deadline:
                    deadline_list.append(deadline)
        else:
            for assignment in Assignment.objects.filter(courses=course.id, journal__user=user).all():
                deadline = create_student_assignment_deadline(user, course, assignment)
                if deadline:
                    deadline_list.append(deadline)

    return responses.success(payload={'deadlines': deadline_list})


@api_view(['GET'])
def get_upcoming_course_deadlines(request, cID):
    """Get upcoming deadlines for the requested user.

    Arguments:
    request -- the request that was send with
    cID -- the course ID that was send with

    Returns a json string with the course deadlines
    """

    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    deadline_list = []

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    for assignment in Assignment.objects.filter(courses=course.id, journal__user=user).all():
        role = permissions.get_role(user, course)

        if role is None:
            return responses.forbidden('You are not in this course.')

        if role.can_grade_journal:
            deadline = create_teacher_assignment_deadline(course, assignment)
            if deadline:
                deadline_list.append(deadline)
        else:
            deadline = create_student_assignment_deadline(user, course, assignment)
            if deadline:
                deadline_list.append(deadline)

    return responses.success(payload={'deadlines': deadline_list})


@api_view(['GET'])
def get_course_permissions(request, cID):
    """Get the permissions of a course.

    Arguments:
    request -- the request that was sent
    cID     -- the course id (string)

    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        if int(cID) >= 0:
            Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    roleDict = permissions.get_permissions(request.user, int(cID))
    if not roleDict:
        return responses.forbidden('You are not participating in this course')

    return responses.success(payload={'permissions': roleDict})


@api_view(['GET'])
def get_nodes(request, jID):
    """Get all nodes contained within a journal.

    Arguments:
    request -- the request that was sent
    jID     -- the journal id

    Returns a json string containing all entry and deadline nodes.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        journal = Journal.objects.get(pk=jID)
    except Journal.DoesNotExist:
        return responses.not_found("Journal does not exist.")

    if not (journal.user == user or permissions.has_assignment_permission(user,
            journal.assignment, 'can_grade_journal')):
        return responses.forbidden('You are not allowed to view journals of other participants.')

    return responses.success(payload={'nodes': edag.get_nodes_dict(journal, request.user)})


@api_view(['GET'])
def get_format(request, aID):
    """Get the format attached to an assignment.

    Arguments:
    request -- the request that was sent
    aID     -- the assignment id

    Returns a json string containing the format.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment does not exist.')

    if not (assignment.courses.all() & user.participations.all()):
        return responses.forbidden('You are not allowed to view this assignment.')

    return responses.success(payload={'format': serialize.format_to_dict(assignment.format)})


@api_view(['GET'])
def get_course_roles(request, cID):
    """Get course roles.

    Arguments:
    request -- the request that was sent.
    cID     -- the course id
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()
    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not allowed to view this course.')
    elif not role.can_edit_course_roles:
        return responses.forbidden('You are not allowed to edit course roles.')

    roles = []

    for role in Role.objects.filter(course=cID):
        roles.append(serialize.role_to_dict(role))
    return responses.success(payload={'roles': roles})


@api_view(['GET'])
def get_user_teacher_courses(request):
    """Get all the courses where the user is a teacher.

    Arguments:
    request -- the request that was sent

    Returns a json string containing the format.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    q_courses = Course.objects.filter(participation__user=request.user.id,
                                      participation__role__can_edit_course=True)
    courses = []
    for course in q_courses:
        courses.append(serialize.course_to_dict(course))
    return responses.success(payload={'courses': courses})


@api_view(['POST'])
def get_names(request):
    """Get names of course, assignment, journal and template.

    Arguments:
    request -- the request that was sent
        cID -- optionally the course id
        aID -- optionally the assignment id
        jID -- optionally the journal id

    Returns a json string containing the names of the set fields.
    cID populates 'course', aID populates 'assignment', tID populates
    'template' and jID populates 'journal' with the users' name.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    cID, aID, jID = utils.optional_params(request.data, "cID", "aID", "jID")
    result = {}

    try:
        if cID:
            course = Course.objects.get(pk=cID)
            role = permissions.get_role(user, course)
            if role is None:
                return responses.forbidden('You are not allowed to view this course.')
            result['course'] = course.name
        if aID:
            assignment = Assignment.objects.get(pk=aID)
            if not (assignment.courses.all() & user.participations.all()):
                return responses.forbidden('You are not allowed to view this assignment.')
            result['assignment'] = assignment.name
        if jID:
            journal = Journal.objects.get(pk=jID)
            if not (journal.user == user or permissions.has_assignment_permission(user,
                    journal.assignment, 'can_grade_journal')):
                return responses.forbidden('You are not allowed to view journals of other participants.')
            result['journal'] = journal.user.username

    except (Course.DoesNotExist, Assignment.DoesNotExist, Journal.DoesNotExist, EntryTemplate.DoesNotExist):
        return responses.not_found('Course, Assignment, Journal or Template does not exist.')

    return responses.success(payload=result)


@api_view(['GET'])
def get_entrycomments(request, eID):
    """Get the comments belonging to the specified entry based on its entryID."""
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry does not exist.')

    if not (entry.node.journal.user == user or permissions.has_assignment_permission(user,
            entry.node.journal.assignment, 'can_grade_journal')):
        return responses.forbidden('You are not allowed to view journals of other participants.')

    entrycomments = EntryComment.objects.filter(entry=entry)

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
    permission = permissions.get_permissions(user, cID=-1)
    if not (permission['is_admin'] or request.user.id == uID):
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
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()
    try:
        assignment = Assignment.objects.get(lti_id=lti_id)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment does not exist.')

    if not permissions.has_assignment_permission(user, assignment, 'can_edit_course'):
        return responses.forbidden('You are not allowed to edit courses.')

    return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


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
