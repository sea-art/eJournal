"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets

import VLE.views.responses as response
from VLE.serializers import StudentAssignmentSerializer, TeacherAssignmentSerializer
from VLE.models import Assignment, Course
import VLE.permissions as permissions
import VLE.utils as utils
import VLE.factory as factory


class AssignmentView(viewsets.ViewSet):
    serializer_class = StudentAssignmentSerializer

    def list(self, request):
        """Get the assignments from a course for the user.

        Arguments:
        request -- request data
            cID -- the ID of the course

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the assignment data
        """
        if not self.request.user.is_authenticated:
            return response.unauthorized()
        try:
            course = Course.objects.get(pk=self.request.cID)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(self.request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')

        if not role.can_grade_journal:
            queryset = course.assignment_set.all()
            serializer = StudentAssignmentSerializer(queryset, many=True)
        else:
            queryset = Assignment.objects.filter(courses=course, journal__user=self.request.user)
            serializer = TeacherAssignmentSerializer(queryset, many=True)

        return response.success(serializer.data)

    def create(self, request):
        """Create a new assignment.

        Arguments:
        request -- the request that was send with
            name -- name of the assignment
            description -- description of the assignment
            cID -- id of the course the assignment belongs to
            points_possible -- the possible amount of points for the assignment

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            key_error -- missing keys

        On success:
            succes -- with the assignment data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            name, description, cID = utils.required_params(request.data, "name", "description", "cID")
            points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
        except KeyError:
            return response.keyerror("name", "description", "cID")

        try:
            Course.objects.get(pk=request.cID)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, cID)

        if role is None:
            return response.unauthorized("You have no access to this course.")
        elif not role.can_add_assignment:
            return response.forbidden('You have no permissions to create an assignment.')

        assignment = factory.make_assignment(name, description, cIDs=[cID],
                                             author=request.user, lti_id=lti_id,
                                             points_possible=points_possible)

        serializer = TeacherAssignmentSerializer(assignment)
        return response.created(serializer.data, obj='assignment')

    def retrieve(self, request, pk=None):
        if pk is None:
            return response.bad_request('pk is missing')
        if not self.request.user.is_authenticated or \
           not self.request.user.participations.filter(pk=pk):
            return response.unauthorized()
        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        serializer = self.serializer_class(assignment)
        return response.success(serializer.data)

    def update(self, request, pk=None):
        if pk is None:
            return response.bad_request('pk is missing')
        # TODO: Check if its a partcipation with the correct rights
        # if not self.request.user.is_authenticated or \
        #    not self.request.user.participations.filter(pk=pk):
        #     return response.unauthorized()
        queryset = Assignment.objects.get(pk)
        serializer = self.serializer_class(queryset)
        return response.success(serializer.data)

    def partial_update(self, request, pk=None):
        print(request)

    def destroy(self, request, pk=None):
        print(request)
