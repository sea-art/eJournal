
import VLE.permissions as permissions
import VLE.views.responses as response
from VLE.serializers import RoleSerializer
from VLE.models import Course, Role
import VLE.factory as factory


class RoleView(object):
    def list(request, pk):
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
            success -- list of all the roles in the course
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

    def partial_update(request, pk):
        """Updates course roles.

        Arguments:
        request -- request data
            roles -- each role of the course that needs to be updated
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- list of all the roles in the course
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('course')

        own_role = permissions.get_role(request.user, course)
        if own_role is None:
            return response.forbidden('You are not in this course.')
        elif not own_role.can_edit_course_roles:
            return response.forbidden('You cannot edit roles of this course.')

        if 'roles' not in request.data:
            return response.keyerror('roles')

        resp = []
        for new_role in request.data['roles']:
            if 'name' not in new_role:
                return response.keyerror('roles.name')
            role = Role.objects.get(name=new_role['name'], course=course)
            serializer = RoleSerializer(role, data=new_role, partial=True)
            if not serializer.is_valid():
                response.bad_request()
            serializer.save()
            resp.append(serializer.data)
        return response.success(resp)

    def create(request, pk):
        """Create course role.

        Arguments:
        request -- request data
            name -- role name
            permissions -- permissions to change (default everything is false)
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- newly created course
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('course')

        own_role = permissions.get_role(request.user, course)
        if own_role is None:
            return response.forbidden('You are not in this course.')
        elif not own_role.can_edit_course_roles:
            return response.forbidden('You cannot create roles of this course.')

        try:
            role = factory.make_role_default_no_perms(request.data['name'], course, **request.data['permissions'])
        except Exception:
            return response.bad_request()
        serializer = RoleSerializer(role, many=False)
        return response.created(serializer.data, obj='role')

    def destroy(request, pk):
        """Delete course role.

        Arguments:
        request -- request data
            name -- role name
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when name is not set
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to edit its roles
        On success:
            success -- newly created course
        """
        if 'name' not in request.data:
            return response.keyerror('name')

        # Users can only delete course roles with can_edit_course_roles
        own_role = permissions.get_role(request.user, pk)
        if own_role is None:
            return response.forbidden(description="You have no access to this course")
        elif not own_role.can_edit_course_roles:
            return response.forbidden(description="You have no permissions to delete this course role.")

        Role.objects.get(name=request.data['name'], course=pk).delete()
        return response.success(message='Succesfully deleted role from course')
