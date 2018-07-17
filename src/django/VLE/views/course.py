"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets

import VLE.views.responses as response
from VLE.serializers import CourseSerializer
from VLE.models import Course
import VLE.permissions as permissions
import VLE.utils as utils
import VLE.factory as factory


class View(viewsets.ViewSet):
    serializer_class = CourseSerializer

    def list(self, request):
        if not self.request.user.is_authenticated:
            return response.unauthorized()
        queryset = self.request.user.participations.all()
        serializer = self.serializer_class(queryset, many=True)
        return response.success(serializer.data)

    def create(self, request):
        if not self.request.user.is_authenticated:
            return response.unauthorized()

        perm = permissions.get_permissions(self.request.user)

        if not perm['can_add_course']:
            return response.forbidden('You have no permissions to create a course.')

        try:
            name, abbr = utils.required_params(request.data, 'name', 'abbr')
            startdate, enddate, lti_id = utils.optional_params(request.data, 'startdate', 'enddate', 'lti_id')
        except KeyError:
            return response.keyerror('name', 'abbr')

        course = factory.make_course(name, abbr, startdate, enddate, request.user, lti_id)

        serializer = self.serializer_class(course, many=False)
        return response.created(serializer)

    def retrieve(self, request, pk=None):
        if not pk:
            return response.bad_request('pk is missing')
        if not self.request.user.is_authenticated or \
           not self.request.user.participations.filter(pk=pk):
            return response.unauthorized()
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('Course')

        serializer = self.serializer_class(course, many=False)
        return response.success(serializer.data)

    def update(self, request, pk=None):
        if not pk:
            return response.bad_request('pk is missing')
        # TODO: Check if its a partcipation with the correct rights
        if not self.request.user.is_authenticated or \
           not self.request.user.participations.filter(pk=pk):
            return response.unauthorized()
        queryset = Course.objects.get(pk)
        serializer = self.serializer_class(queryset, many=False)
        return response.success(serializer.data)

    def partial_update(self, request, pk=None):
        print(request)

    def destroy(self, request, pk=None):
        print(request)
