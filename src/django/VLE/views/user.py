"""
user.py.

In this file are all the user api requests.
"""
from rest_framework import viewsets

from VLE.serializers import UserSerializer
from VLE.models import User


class View(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
