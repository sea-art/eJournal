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
