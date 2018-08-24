"""
get.py.

API functions that handle the get requests.
"""
from rest_framework.decorators import api_view
from django.conf import settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.shortcuts import redirect
import datetime

import statistics as st
import json
import jwt

import VLE.lti_launch as lti
import VLE.edag as edag
import VLE.utils.generic_utils as utils
import VLE.utils.file_handling as file_handling
from VLE.models import Assignment, Course, Journal, EntryTemplate, EntryComment, User, Node, \
    Role, Entry, UserFile
import VLE.serializers as serialize
import VLE.permissions as permissions
import VLE.views.responses as responses

# VUE ENTRY STATE
BAD_AUTH = '-1'

NO_USER = '0'
LOGGED_IN = '1'

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
        return responses.not_found('Course not found.')

    if not permissions.is_user_in_course(user, q_course):
        return responses.forbidden('You are not a participant of this course.')

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
        return responses.not_found('Course not found.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not a participant of this course.')
    elif not role.can_view_course_participants:
        return responses.forbidden('You cannot view the participants in this course.')

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
        return responses.not_found('Course not found.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not a participant of this course.')
    elif not role.can_view_course_participants:
        return responses.forbidden('You cannot view the participants in this course.')

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
        return responses.not_found('Course not found.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not a participant of this course.')

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
        return responses.not_found('Course not found.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not a participant of this course.')

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment not found.')

    if role.can_grade_journal:
        return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})
    else:
        return responses.success(payload={'assignment': serialize.student_assignment_to_dict(assignment, request.user)})


@api_view(['GET'])
def get_assignment_journals(request, aID):
    """Get the student submitted journals of one assignment.

    Arguments:
    request -- the request that was send with
    aID -- the assignment ID to get the journals from

    Returns a json string with the journals
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment not found.')

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

    return responses.success(payload={'stats': stats if stats else None, 'journals': journals})


@api_view(['GET'])
def get_journal(request, jID):
    """Get a student submitted journal.

    Arguments:
    request -- the request that was send with
    jID -- the journal ID to get

    Returns a journal.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        journal = Journal.objects.get(pk=jID)
    except journal.DoesNotExist:
        return responses.not_found('Journal not found.')

    if not (journal.user == user or permissions.has_assignment_permission(user, journal.assignment,
                                                                          'can_view_assignment_participants')):
        return responses.forbidden('You are not allowed to view this journal.')

    return responses.success(payload={'journal': serialize.journal_to_dict(journal)})


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
    journal = {}

    try:
        journal = Journal.objects.get(assignment=assignment, user=user)
    except Journal.DoesNotExist:
        return {}

    deadlines = journal.node_set.exclude(preset=None).values('preset__deadline')
    if len(deadlines) == 0:
        return {}

    # Gets the node with the earliest deadline
    future_deadlines = deadlines.filter(preset__deadline__gte=datetime.datetime.now()).order_by('preset__deadline')

    if len(future_deadlines) == 0:
        return {}

    future_deadline = future_deadlines[0]

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
            return responses.forbidden('You are not a participant of this course.')

        if role.can_grade_journal:
            for assignment in Assignment.objects.filter(courses=course.id).all():
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
        return responses.not_found('Course not found.')

    for assignment in Assignment.objects.filter(courses=course.id, journal__user=user).all():
        role = permissions.get_role(user, course)

        if role is None:
            return responses.forbidden('You are not a participant of this course.')

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
        return responses.not_found('Course not found.')

    roleDict = permissions.get_permissions(request.user, int(cID))
    if not roleDict:
        return responses.forbidden('You are not participating in this course')

    return responses.success(payload={'permissions': roleDict})


@api_view(['GET'])
def get_assignment_permissions(request, aID):
    """Get the permissions of an assignment.

    Arguments:
    request -- the request that was sent
    aID     -- the assignment id (string)

    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        if int(aID) >= 0:
            Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment not found.')

    roleDict = permissions.get_assignment_id_permissions(request.user, int(aID))
    if not roleDict:
        return responses.forbidden('You are not participating in any courses with this assignment')

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
        return responses.not_found('Journal not found.')

    if not (journal.user == user or permissions.has_assignment_permission(user,
            journal.assignment, 'can_view_assignment_participants')):
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
        return responses.not_found('Assignment not found.')

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
        return responses.not_found('Course not found.')

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
    """Get names of course, assignment, journal.

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
                    journal.assignment, 'can_view_assignment_participants')):
                return responses.forbidden('You are not allowed to view journals of other participants.')
            result['journal'] = journal.user.first_name + " " + journal.user.last_name

    except (Course.DoesNotExist, Assignment.DoesNotExist, Journal.DoesNotExist, EntryTemplate.DoesNotExist):
        return responses.not_found('Course, Assignment, Journal or Template')

    return responses.success(payload=result)


@api_view(['GET'])
def get_entrycomments(request, eID):
    """Get the comments belonging to the specified entry based on its eID."""
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry not found.')

    if not (entry.node.journal.user == user or permissions.has_assignment_permission(user,
            entry.node.journal.assignment, 'can_view_assignment_participants')):
        return responses.forbidden('You are not allowed to view journals of other participants.')

    if permissions.has_assignment_permission(user, entry.node.journal.assignment,
                                             'can_grade_journal'):
        entrycomments = EntryComment.objects.filter(entry=entry)
    else:
        entrycomments = EntryComment.objects.filter(entry=entry, published=True)

    return responses.success(payload={
        'entrycomments': [serialize.entrycomment_to_dict(comment) for comment in entrycomments]
        })


@api_view(['GET'])
def get_user_data(request, uID):
    """Get the user data of the given user.

    Get the users profile data and posted entries with the titles of the journals of the user based on the uID. As well
    as all the user uploaded files.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    user = User.objects.get(pk=uID)

    # Check the right permissions to get this users data, either be the user of the data or be an admin.
    permission = permissions.get_permissions(user, cID=-1)
    if not (permission['is_superuser'] or request.user.id == uID):
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

    archive_path, content_type = file_handling.compress_all_user_data(user,
                                                                      {'profile': profile, 'journals': journal_dict})

    return responses.file_b64(archive_path, content_type)


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
        return responses.not_found('Assignment not found.')

    if not permissions.has_assignment_permission(user, assignment, 'can_edit_course'):
        return responses.forbidden('You are not allowed to edit the course.')

    return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['GET'])
def get_lti_params_from_jwt(request, jwt_params):
    """Handle the controlflow for course/assignment create, connect and select.

    Returns the data needed for the correct entry place.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    user = request.user
    lti_params = jwt.decode(jwt_params, settings.LTI_SECRET, algorithms=['HS256'])
    roles = json.load(open('config.json'))
    lti_roles = dict((roles[k], k) for k in roles)
    role = lti_roles[lti_params['roles']]

    payload = dict()
    course = lti.check_course_lti(lti_params, user, role)
    if course is None:
        if role == 'Teacher':
            payload['state'] = NEW_COURSE
            payload['lti_cName'] = lti_params['context_title']
            payload['lti_abbr'] = lti_params['context_label']
            payload['lti_cID'] = lti_params['context_id']
            payload['lti_aName'] = lti_params['resource_link_title']
            payload['lti_aID'] = lti_params['resource_link_id']

            if 'custom_canvas_assignment_points_possible' in lti_params:
                payload['lti_points_possible'] = lti_params['custom_canvas_assignment_points_possible']

            return responses.success(payload={'params': payload})
        else:
            return responses.not_found(description='The assignment you are looking for cannot be found. \
                <br>Note: it might still be reachable through the assignment section')

    assignment = lti.check_assignment_lti(lti_params)
    if assignment is None:
        if role == 'Teacher':
            payload['state'] = NEW_ASSIGN
            payload['cID'] = course.pk
            payload['lti_aName'] = lti_params['resource_link_title']
            payload['lti_aID'] = lti_params['resource_link_id']

            if 'custom_canvas_assignment_points_possible' in lti_params:
                payload['lti_points_possible'] = lti_params['custom_canvas_assignment_points_possible']

            return responses.success(payload={'params': payload})
        else:
            return responses.not_found(description='The assignment you are looking for cannot be found. \
                <br>Note: it might still be reachable through the assignment section')

    journal = lti.select_create_journal(lti_params, user, assignment, roles)
    jID = journal.pk if journal is not None else None
    state = FINISH_T if jID is None else FINISH_S

    payload['state'] = state
    payload['cID'] = course.pk
    payload['aID'] = assignment.pk
    payload['jID'] = jID
    return responses.success(payload={'params': payload})


@api_view(['POST'])
def lti_launch(request):
    """Django view for the lti post request.

    handles the users login or sned to a creation page.
    """
    secret = settings.LTI_SECRET
    key = settings.LTI_KEY

    authenticated, err = lti.OAuthRequestValidater.check_signature(
        key, secret, request)

    if authenticated:
        roles = json.load(open('config.json'))
        params = request.POST.dict()
        user = lti.check_user_lti(params, roles)

        params['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
        lti_params = jwt.encode(params, secret, algorithm='HS256').decode('utf-8')

        if user is None:
            q_names = ['state', 'lti_params']
            q_values = [NO_USER, lti_params]

            if 'lis_person_name_full' in params:
                fullname = params['lis_person_name_full']
                splitname = fullname.split(' ')
                firstname = splitname[0]
                lastname = fullname[len(splitname[0])+1:]
                q_names += ['firstname', 'lastname']
                q_values += [firstname, lastname]

            if 'lis_person_sourcedid' in params:
                q_names.append('username')
                q_values.append(params['lis_person_sourcedid'])

            if 'lis_person_contact_email_primary' in params:
                q_names.append('email')
                q_values.append(params['lis_person_contact_email_primary'])

            return redirect(lti.create_lti_query_link(q_names, q_values))

        refresh = TokenObtainPairSerializer.get_token(user)
        print(refresh)
        access = refresh.access_token
        return redirect(lti.create_lti_query_link(['lti_params', 'jwt_access', 'jwt_refresh', 'state'],
                                                  [lti_params, access, refresh, LOGGED_IN]))

    return redirect(lti.create_lti_query_link(['state'], [BAD_AUTH]))


@api_view(['GET'])
def get_user_file(request, file_name, author_uID):
    """Get a user file by name if it exists.

    Arguments:
    request -- the request that was sent
    file_name -- the name of the file without any specified path.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        user_file = UserFile.objects.get(author=int(author_uID), file_name=file_name)
    except UserFile.DoesNotExist:
        return responses.bad_request(file_name + ' was not found.')

    if user_file.author.id is user.id or \
       permissions.has_assignment_permission(user, user_file.assignment, 'can_view_assignment_participants'):
        return responses.user_file_b64(user_file)
    else:
        return responses.unauthorized('Unauthorized to view: %s by author ID: %s.' % (file_name, author_uID))
