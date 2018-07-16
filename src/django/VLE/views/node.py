"""
node.py.

In this file are all the node api requests.
"""
from rest_framework import viewsets

from VLE.serializers import NodeSerializer
from VLE.models import Node


class View(viewsets.ModelViewSet):
    serializer_class = NodeSerializer

    def get_queryset(self):
        return Node.objects.all()
