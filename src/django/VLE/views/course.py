"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets

from VLE.serializers import CourseSerializer


class View(viewsets.ModelViewSet):
    serializer_class = CourseSerializer

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return None
        return self.request.user.participations.all()
