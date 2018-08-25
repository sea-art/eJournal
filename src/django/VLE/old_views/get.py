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
