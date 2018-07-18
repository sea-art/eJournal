"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets

import VLE.views.responses as response
from VLE.serializers import StudentAssignmentSerializer, TeacherAssignmentSerializer
from VLE.models import Assignment, Course
import VLE.permissions as permissions


class AssignmentView(viewsets.ViewSet):
    serializer_class = StudentAssignmentSerializer

    def list(self, request):
        # if not self.request.user.is_authenticated:
        #     return response.unauthorized()
        try:
            course = Course.objects.get(pk=self.request.cID)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(self.request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')

        if role.can_grade_journal:
            queryset = course.assignment_set.all()
            serializer = StudentAssignmentSerializer(queryset, many=True)
        else:
            queryset = Assignment.objects.filter(courses=course, journal__user=self.request.user)
            serializer = TeacherAssignmentSerializer(queryset, many=True)

        return response.success(serializer.data)

    def create(self, request):
        print(request)

    def retrieve(self, request, pk=None):
        if not pk:
            return response.bad_request('pk is missing')
        # if not self.request.user.is_authenticated or \
        #    not self.request.user.participations.filter(pk=pk):
        #     return response.unauthorized()
        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        serializer = self.serializer_class(assignment, many=False)
        return response.success(serializer.data)

    def update(self, request, pk=None):
        if not pk:
            return response.bad_request('pk is missing')
        # TODO: Check if its a partcipation with the correct rights
        # if not self.request.user.is_authenticated or \
        #    not self.request.user.participations.filter(pk=pk):
        #     return response.unauthorized()
        queryset = Assignment.objects.get(pk)
        serializer = self.serializer_class(queryset, many=False)
        return response.success(serializer.data)

    def partial_update(self, request, pk=None):
        print(request)

    def destroy(self, request, pk=None):
        print(request)
