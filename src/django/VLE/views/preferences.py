"""
user.py.

In this file are all the user api requests.
"""
from smtplib import SMTPAuthenticationError

from django.conf import settings
from django.core.validators import validate_email
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

import VLE.factory as factory
import VLE.lti_launch as lti_launch
import VLE.permissions as permissions
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
import VLE.validators as validators
from VLE.models import (Assignment, Content, Entry, Instance, Journal, Node,
                        Preferences, User, UserFile)
from VLE.serializers import PreferencesSerializer


class PreferencesView(viewsets.ViewSet):
    def retrieve(self, request, pk):
        """Get the preferences of the requested user.

        Arguments:
        request -- request data
        pk -- user ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the user doesn't exist
        On success:
            success -- with the preferences data
        """
        if int(pk) == 0:
            pk = request.user.id
        if not (request.user.id == pk or request.user.is_superuser):
            return response.forbidden('You are not allowed to view this users preferences.')

        preferences = Preferences.objects.get(pk=pk)
        serializer = PreferencesSerializer(preferences)

        return response.success({'preferences': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing user.

        Arguments:
        request -- request data
            jwt_params -- jwt params to get the lti information from
                user_id -- id of the user
                user_image -- user image
                roles -- role of the user
        pk -- user ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when the user is not superuser or pk is not the same as the logged in user
            not found -- when the user doesnt exists
            bad request -- when the data is invalid
        On success:
            success -- with the updated user
        """
        pk, = utils.required_typed_params(kwargs, (int, 'pk'))
        if pk == 0:
            pk = request.user.id
        if not (request.user.id == pk or request.user.is_superuser):
            return response.forbidden('You are not allowed to change this users preferences.')

        preferences = Preferences.objects.get(user=pk)
        serializer = PreferencesSerializer(preferences, data=request.data, partial=True)

        if not serializer.is_valid():
            return response.bad_request()

        serializer.save()

        return response.success({'preferences': serializer.data})
