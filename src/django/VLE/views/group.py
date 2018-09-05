"""
group.py.

In this file are all the group api requests.
"""
from rest_framework import viewsets
# from rest_framework.decorators import action

import VLE.serializers as serialize
import VLE.views.responses as response
from VLE.models import Course, Group
import VLE.permissions as permissions
import VLE.utils.generic_utils as utils
import VLE.factory as factory


class GroupView(viewsets.ViewSet):

    def create(self, request):
        """Create a new course group.

        Arguments:
        request -- the request that was send with
            name -- name of the course group
            cID -- course ID of the course
            lti_id -- (optional) lti_id to link the course to

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when the user has no permission to create new groups
        On success, with the course group.
        """
        user = request.user
        if not user.is_authenticated:
            return response.unauthorized()

        try:
            name, cID = utils.required_params(request.data, "name", "cID")
            lti_id = utils.optional_params(request.data, 'lti_id')
        except KeyError:
            return response.keyerror("name", "cID")

        # TODO Look for which permission check is better
        # role = permissions.get_role(user, cID)
        # if not role.can_add_course_user_group:
        #     return response.forbidden("You have no permissions to create a course group.")
        perm = permissions.get_permissions(request.user)
        if not perm['can_add_course_group']:
            return response.forbidden('You have no permissions to create a course.')

        try:
            course = Course.objects.get(pk=cID)
        except Course.DoesNotExist:
            return response.not_found('Course does not exist.')

        if Group.objects.get(name=name, course=course):
            return response.bad_request('Course group already exists')
        else:
            course_group = factory.make_course_group(name, course, lti_id)

        return response.created(payload={'course': serialize.group_to_dict(course_group)})
