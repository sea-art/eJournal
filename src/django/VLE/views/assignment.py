"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets

from VLE.serializers import AssignmentSerializer
from VLE.models import Assignment


class View(viewsets.ModelViewSet):
    serializer_class = AssignmentSerializer

    def get_queryset(self):
        return Assignment.objects.all()
