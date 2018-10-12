
from rest_framework import viewsets

import VLE.factory as factory
import VLE.permissions as permissions
import VLE.utils.generic_utils as utils
import VLE.views.responses as response
from VLE.models import Assignment, Course, Role, User
from VLE.serializers import RoleSerializer
from VLE.utils.error_handling import VLEMissingRequiredKey, VLEParamWrongType


class RoleView(viewsets.ViewSet):
    def list(self, request):
        """Get course roles.

        Arguments:
        request -- request data
            course_id -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- list of all the roles in the course

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        course_id = request.query_params['course_id']
        course = Course.objects.get(pk=course_id)

        if not request.user.has_permission('can_edit_course_roles', course):
            return response.forbidden('You are not allowed to edit course roles.')

        roles = Role.objects.filter(course=course)
        serializer = RoleSerializer(roles, many=True)
        return response.success({'roles': serializer.data})

    def retrieve(self, request, pk=0):
        """Get the permissions of a user connected to a course / assignment.

        Arguments:
        request -- the request that was sent
            course_id -- course ID
            assignment_id -- assignment ID
        pk -- user ID (0 = logged in user)

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course is not found
            forbidden -- when the user is not in the course
        On success:
            success -- with a list of the permissions

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if int(pk) == 0:
            pk = request.user.id

        user = User.objects.get(pk=pk)

        # Return course permissions if course_id is set
        try:
            course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
            if course_id > 0:
                course = Course.objects.get(pk=course_id)
                if permissions.is_participant(user, course):
                    return response.forbidden('You are not a participant of this course.')

                return response.success({'role': permissions.serialize_course_permissions(request.user, course)})
        # Return assignment permissions if assignment_id is set
        except (VLEMissingRequiredKey, VLEParamWrongType):
            assignment_id, = utils.required_typed_params(request.query_params, (int, 'assignment_id'))
            assignment = Assignment.objects.get(pk=assignment_id)

            return response.success({'role': permissions.serialize_assignment_permissions(request.user, assignment)})
        # Returns keyerror if course_id nor assignment_id is set

    def create(self, request):
        """Create course role.

        Arguments:
        request -- request data
            course_id -- course ID
            name -- role name
            permissions -- permissions to change (default everything is false)

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- newly created course

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        course = Course.objects.get(pk=request.data['course_id'])

        if not request.user.has_permission('can_edit_course_roles', course):
            return response.forbidden('You do not have the permission to create roles for this course.')

        try:
            role = factory.make_role_default_no_perms(request.data['name'], course, **request.data['permissions'])
        except Exception:
            # Dubious code...
            return response.bad_request()

        serializer = RoleSerializer(role, many=False)
        return response.created({'role': serializer.data})

    def partial_update(self, request, pk):
        """Updates course roles.

        Arguments:
        request -- request data
            roles -- each role of the course that needs to be updated
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
            bad_request -- if
        On success:
            success -- list of all the roles in the course

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        course = Course.objects.get(pk=pk)

        if not request.user.has_permission('can_edit_course_roles', course):
            return response.forbidden('You cannot edit roles of this course.')

        resp = []

        for new_role in request.data['roles']:
            try:
                role = Role.objects.get(name=new_role['name'], course=course)
            except Role.DoesNotExist:
                role = factory.make_role_default_no_perms(new_role['name'], course)
            serializer = RoleSerializer(role, data=new_role, partial=True)
            if not serializer.is_valid():
                response.bad_request()

            serializer.save()

            resp.append(serializer.data)
        return response.success({'roles': resp})

    def destroy(self, request, pk):
        """Delete course role.

        Arguments:
        request -- request data
            name -- role name
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- newly created course

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        name = request.query_params['name']
        course = Course.objects.get(pk=pk)

        # Users can only delete course roles with can_edit_course_roles
        if not request.user.has_permission('can_edit_course_roles', course):
            return response.forbidden(description="You have no permissions to delete this course role.")

        if name in ['Student', 'TA', 'Teacher']:
            return response.bad_request("Default roles 'Student', 'TA' and 'Teacher' cannot be deleted.")

        Role.objects.get(name=name, course=pk).delete()
        return response.success(description='Succesfully deleted role from course.')
