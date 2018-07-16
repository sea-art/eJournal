"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets

from django.shortcuts import get_object_or_404

import VLE.views.responses as response
from VLE.serializers import CourseSerializer
from VLE.models import Course


class View(viewsets.ViewSet):
    serializer_class = CourseSerializer

    def list(self, request):
        if not self.request.user.is_authenticated:
            return response.unauthorized()
        queryset = self.request.user.participations.all()
        serializer = self.serializer_class(queryset, many=True)
        return response.success(serializer.data)

    def create(self, request):
        print(request)

    def retrieve(self, request, pk=None):
        if not pk:
            return response.bad_request('pk is missing')
        # if not self.request.user.is_authenticated or \
        #    not self.request.user.participations.filter(pk=pk):
        #     return response.unauthorized()
        queryset = Course.objects.all()
        course = get_object_or_404(queryset, pk=pk)
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
