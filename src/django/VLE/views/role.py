
from rest_framework import viewsets

import VLE.permissions as permissions
import VLE.views.responses as response
from VLE.serializers import RoleSerializer
from VLE.models import Course, Role, Assignment, User
import VLE.factory as factory


class RoleView(viewsets.ViewSet):
    def list(self, request):
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
            course_id = request.query_params['cID']
        except KeyError:
            return response.keyerror('cID')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not allowed to view this course.')
        elif not role.can_edit_course_roles:
            return response.forbidden('You are not allowed to edit course roles.')

        roles = Role.objects.filter(course=course_id)
        serializer = RoleSerializer(roles, many=True)
        return response.success(serializer.data)

    def partial_update(self, request, pk):
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

    def retrieve(self, request, pk=0):
        """Get the permissions of a user connected to a course / assignment.

        Arguments:
        request -- the request that was sent
            cID -- course ID
            aID -- assignment ID
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

        try:
            user = request.user if int(pk) == 0 else User.objects.get(int(pk))
        except User.DoesNotExist:
            return response.not_found('User')

        try:
            course_id = request.query_params['cID']
        except KeyError:
            try:
                assignment_id = request.query_params['aID']
                try:
                    assignment = Assignment.objects.get(pk=assignment_id)
                    result = {}
                    for course in assignment.courses.all():
                        result = {key: value or (result[key] if key in result and result[key] else False)
                                  for key, value in permissions.get_permissions(user, course.pk).items()}
                    return response.success(result)
                except Course.DoesNotExist:
                    return response.not_found('Course')
            except KeyError:
                return response.keyerror('cID or aID')

        try:
            if int(course_id) > 0:
                Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return response.not_found('Course')

        roleDict = permissions.get_permissions(user, int(course_id))
        if not roleDict:
            return response.forbidden('You are not participating in this course')

        return response.success(roleDict)

    def create(self, request, pk):
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

    def destroy(self, request, pk):
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
