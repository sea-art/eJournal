"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets
from rest_framework.decorators import action

import VLE.views.responses as response
from VLE.serializers import CourseSerializer
from VLE.serializers import UserSerializer
from VLE.models import Course, User, Role, Journal
import VLE.permissions as permissions
import VLE.utils as utils
import VLE.factory as factory
from VLE.views.roles import RoleView


class CourseView(viewsets.ViewSet):
    serializer_class = CourseSerializer

    def list(self, request):
        """Get the courses that the user participates in.

        Arguments:
        request -- request data

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
        On succes:
            success -- with the course data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        queryset = request.user.participations.all()
        serializer = self.serializer_class(queryset, many=True)
        return response.success(serializer.data)

    def create(self, request):
        """Create a new course.

        Arguments:
        request -- request data
            name -- name of the course
            abbr -- abbreviation of the course
            startdate -- (optional) date when the course starts
            enddate -- (optional) date when the course ends
            lti_id -- (optional) lti_id to link the course to

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when the user has no permission to create new courses
        On succes:
            success -- with the course data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        perm = permissions.get_permissions(request.user)

        if not perm['can_add_course']:
            return response.forbidden('You have no permissions to create a course.')

        try:
            name, abbr = utils.required_params(request.data, 'name', 'abbr')
            startdate, enddate, lti_id = utils.optional_params(request.data, 'startdate', 'enddate', 'lti_id')
        except KeyError:
            return response.keyerror('name', 'abbr')

        course = factory.make_course(name, abbr, startdate, enddate, request.user, lti_id)

        serializer = self.serializer_class(course, many=False)
        return response.created(serializer.data, obj='course')

    def retrieve(self, request, pk=None):
        """Get the course data from the course ID.

        Arguments:
        request -- request data
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
        On success:
            success -- with the course data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('Course')

        if not permissions.is_user_in_course(request.user, course):
            return response.forbidden('You are not in this course.')

        serializer = self.serializer_class(course, many=False)
        return response.success(serializer.data)

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        """Update an existing course.

        Arguments:
        request -- request data
            data -- the new data for the course
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            unauthorized -- when the user is unauthorized to edit the course
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new course data
        """
        pk = kwargs.get('pk')
        # TODO: Check if its a partcipation with the correct rights
        if not request.user.is_authenticated or \
           not request.user.participations.filter(pk=pk):
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('course')

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')
        elif not role.can_edit_course:
            return response.unauthorized('You are unauthorized to edit this course.')

        serializer = self.serializer_class(course, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()
        return response.success(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete an existing course.

        Arguments:
        request -- request data
        pk -- course ID

        Returns:
        On failure:
            not found -- when the course does not exists
            unauthorized -- when the user is not logged in
            forbidden -- when the user is not in the course
        On success:
            success -- with a message that the course was deleted
        """
        pk = kwargs.get('pk')
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('course')

        role = permissions.get_role(request.user, pk)
        if role is None:
            return response.unauthorized(description="You are unauthorized to view this course.")
        elif not role.can_delete_course:
            return response.forbidden(description="You are unauthorized to delete this course.")

        course.delete()
        return response.deleted('course')

    @action(methods=['get'], detail=False)
    def linkable(self, request):
        """Get linkable courses.

        Get all courses that the current user is connected to and where the lti_id equals to NULL.
        A user can then link this course to Canvas.

        Arguments:
        request -- request data

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
        On success:
            success -- with a message that the course was deleted
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if not request.user.is_teacher:
            return response.forbidden("You are not allowed to link courses.")

        unlinked_courses = Course.objects.filter(participation__user=request.user.id,
                                                 participation__role__can_edit_course=True,
                                                 lti_id=None)

        serializer = UserSerializer(unlinked_courses, many=True)
        return response.success(serializer.data)

    @action(methods=['get'], detail=True)
    def users(self, request, pk=None):
        """Get all users and their roles for a given course.

        Arguments:
        request -- request data
        pk -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not in the course
            forbidden -- when the user is unauthorized to view its participants
        On success:
            success -- list of all the users and their role
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')
        elif not role.can_view_course_participants:
            return response.forbidden('You cannot view participants in this course.')

        queryset = course.users
        serializer = UserSerializer(queryset, many=True)
        # TODO: Include role of participation
        return response.success(serializer.data)

    @action(methods=['get', 'patch'], detail=True)
    def roles(self, request, pk):
        if request.method == 'GET':
            return RoleView.list(request, pk)
        elif request.method == 'PATCH':
            return RoleView.partial_update(request, pk)
        elif request.method == 'post':
            return RoleView.create(request, pk)
        return response.bad_request('Invalid method')

    @action(methods=['get'], detail=False)
    def is_teacher(self, request):
        """Get all the courses where the user is a teacher.

        Arguments:
        request -- request data

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
        On success:
            success -- list of all the courses where the user is a teacher
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        courses = Course.objects.filter(participation__user=request.user.id,
                                        participation__role__can_edit_course=True)
        serializer = CourseSerializer(courses, many=True)
        return response.success(serializer.data)

    @action(methods=['patch'], detail=True)
    def add_user(self, request, pk):
        """Add a user to a course.

        Arguments:
        request -- request data
            uID -- student ID given with the request
            role -- name of the role (default: Student)

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when course or user is not found
            forbidden -- when the logged in user is not connected to the course
            bad request -- when the new user is already connected to the course
            not found -- when the role doesnt exist
        On success:
            success -- success message
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            user_id = utils.required_params(request.data, 'uID')
            role_name = utils.optional_params(request.data, 'role') or 'Student'
        except KeyError:
            return response.keyerror('uID')

        try:
            user = User.objects.get(pk=user_id)
            course = Course.objects.get(pk=pk)
        except (User.DoesNotExist, Course.DoesNotExist):
            return response.not_found('user or course')

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')
        elif not role.can_add_course_participants:
            return response.forbidden('You cannot add users to this course.')

        if permissions.is_user_in_course(user, course):
            return response.bad_request('User already participates in the course.')

        try:
            role = Role.objects.get(name=role_name, course=course)
        except Role.DoesNotExist:
            return response.not_found()
        factory.make_participation(user, course, role)

        assignments = course.assignment_set.all()
        role = permissions.get_role(user, pk)
        if role.can_edit_journal:
            for assignment in assignments:
                if not Journal.objects.filter(assignment=assignment, user=user).exists():
                    factory.make_journal(assignment, user)
        return response.success(message='Succesfully added student to course')
