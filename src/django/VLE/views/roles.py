
import VLE.permissions as permissions
import VLE.views.responses as response
from VLE.serializers import RoleSerializer
from VLE.models import Course, Role


class RoleView(object):
    def list(self, request, pk):
        """Get course roles.

        Arguments:
        request -- request data
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- list of all the roles in a course
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not allowed to view this course.')
        elif not role.can_edit_course_roles:
            return response.forbidden('You are not allowed to edit course roles.')

        roles = Role.objects.filter(course=pk)
        serializer = RoleSerializer(roles, many=True)
        return response.success(serializer.data)

    def partial_update(self, request, pk):
        """Updates course roles.

        Arguments:
        request -- request data
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- list of all the roles in a course
        """
        user = request.user
        if not user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('course')

        role = permissions.get_role(user, course)
        if role is None:
            return response.forbidden('You are not in this course.')
        elif not role.can_edit_course_roles:
            return response.forbidden('You cannot edit roles of this course.')

        serializer = self.serializer_class(course, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()
        return response.success(serializer.data)
        # for role in request.data['roles']:
        #     db_role = Role.objects.filter(name=role['name'])
        #     if not db_role:
        #         factory.make_role_default_no_perms(role['name'], Course.objects.get(pk=cID), **role['permissions'])
        #     else:
        #         permissions.edit_permissions(db_role[0], **role['permissions'])
        # return responses.success()
