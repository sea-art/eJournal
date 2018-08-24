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


# @api_view(['GET'])
# def get_unenrolled_users(request, cID):
#     """Get all users not connected to a given course.
#
#     Arguments:
#     request -- the request
#     cID -- the course ID
#
#     Returns a json string with a list of participants.
#     """
#     user = request.user
#     if not user.is_authenticated:
#         return responses.unauthorized()
#
#     try:
#         course = Course.objects.get(pk=cID)
#     except Course.DoesNotExist:
#         return responses.not_found('Course not found.')
#
#     role = permissions.get_role(user, course)
#     if role is None:
#         return responses.forbidden('You are not a participant of this course.')
#     elif not role.can_view_course_participants:
#         return responses.forbidden('You cannot view the participants in this course.')
#
#     ids_in_course = course.participation_set.all().values('user__id')
#     result = User.objects.all().exclude(id__in=ids_in_course)
#
#     return responses.success(payload={'users': [serialize.user_to_dict(user) for user in result]})
#
#
# def create_teacher_assignment_deadline(course, assignment):
#     """Creates and returns the earliest deadline with data of an assignment
#        from a teacher.
#
#     Arguments:
#     coures -- the course save information in the dictionary
#     cID -- the assignment to get the deadlines
#
#     Returns a dictionary with information of the assignment deadline.
#     """
#     journals = []
#
#     for journal in assignment.journal_set.all():
#         journals.append(serialize.journal_to_dict(journal))
#
#     totalNeedsMarking = sum([x['stats']['submitted'] - x['stats']['graded'] for x in journals])
#
#     format = serialize.format_to_dict(assignment.format)
#     if len(format['presets']) == 0:
#         return {}
#
#     deadline_data = format['presets'][0]['deadline']
#     splitted_deadline = deadline_data.split(' ')
#     deadline = [splitted_deadline[0],
#                 splitted_deadline[1].split(':')[0],
#                 splitted_deadline[1].split(':')[1]]
#     deadline = {'Date': deadline[0],
#                 'Hours': deadline[1],
#                 'Minutes': deadline[2]
#                 }
#
#     return {'name': serialize.assignment_to_dict(assignment)['name'],
#             'courseAbbr': course.abbreviation,
#             'cID': course.id,
#             'aID': assignment.id,
#             'deadline': deadline,
#             'totalNeedsMarking': totalNeedsMarking}
#
#
# def create_student_assignment_deadline(user, course, assignment):
#     """Creates and returns the earliest deadline with data of an assignment
#        from a student.
#
#     Arguments:
#     coures -- the course save information in the dictionary
#     cID -- the assignment to get the deadlines
#
#     Returns a dictionary with information of the assignment deadline.
#     """
#     journal = {}
#
#     try:
#         journal = Journal.objects.get(assignment=assignment, user=user)
#     except Journal.DoesNotExist:
#         return {}
#
#     deadlines = journal.node_set.exclude(preset=None).values('preset__deadline')
#     if len(deadlines) == 0:
#         return {}
#
#     # Gets the node with the earliest deadline
#     future_deadlines = deadlines.filter(preset__deadline__gte=datetime.datetime.now()).order_by('preset__deadline')
#
#     if len(future_deadlines) == 0:
#         return {}
#
#     future_deadline = future_deadlines[0]
#
#     future_deadline = {'Date': future_deadline['preset__deadline'].date(),
#                        'Hours': future_deadline['preset__deadline'].hour,
#                        'Minutes': future_deadline['preset__deadline'].minute}
#
#     return {'name': serialize.assignment_to_dict(assignment)['name'],
#             'courseAbbr': course.abbreviation,
#             'cID': course.id,
#             'aID': assignment.id,
#             'jID': journal.id,
#             'deadline': future_deadline,
#             'totalNeedsMarking': 0}




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
        entrycomments = Comment.objects.filter(entry=entry)
    else:
        entrycomments = Comment.objects.filter(entry=entry, published=True)

    return responses.success(payload={
        'entrycomments': [serialize.entrycomment_to_dict(comment) for comment in entrycomments]
        })


# TODO: Test is current implementation in recieve in views/assignment.py works
# @api_view(['GET'])
# def get_assignment_by_lti_id(request, lti_id):
#     """Get an assignment if it exists.
#
#     Arguments:
#     request -- the request that was sent
#     lti_id -- lti_id of the assignment
#     """
#     user = request.user
#     if not user.is_authenticated:
#         return responses.unauthorized()
#     try:
#         assignment = Assignment.objects.get(lti_id=lti_id)
#     except Assignment.DoesNotExist:
#         return responses.not_found('Assignment')
#
#     if not permissions.has_assignment_permission(user, assignment, 'can_edit_course'):
#         return responses.forbidden('You are not allowed to edit the courses.')
#
#     return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


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
