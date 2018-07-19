"""
user.py.

In this file are all the user api requests.
"""
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from rest_framework import viewsets
from rest_framework.decorators import action

from VLE.serializers import UserSerializer
from VLE.serializers import OwnUserSerializer
from VLE.models import User
from VLE.views import responses as response
import VLE.utils as utils
import VLE.factory as factory

import re
import jwt
import json


def validate_password(password):
    """Validate the give password.

    Arguments:
    password -- the password to validate

    Returns:
    On failure:
        string -- with the part of the password that is not valid
    On succes:
        None
    """
    if len(password) < 8:
        return 'Password needs to contain at least 8 characters.'
    if password == password.lower():
        return 'Password needs to contain at least 1 capital letter.'
    if re.match(r'^\w+$', password):
        return 'Password needs to contain a special character.'
    return None


class UserView(viewsets.ViewSet):
    serializer_class = UserSerializer

    def list(self, request):
        """Get all the users.

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

        serializer = self.serializer_class(User.objects.all(), many=True)
        return response.success(serializer.data)

    def retrieve(self, request, pk):
        """Get the user data of the given user.

        Get the profile data and posted entries with the titles of the journals.
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return response.not_found('user')

        if request.user.pk is int(pk):
            serializer = OwnUserSerializer(user, many=False)
        else:
            serializer = self.serializer_class(user, many=False)
        return response.success(serializer.data)

    def create(self, request):
        """Create a new user.

        Arguments:
        request -- request data
            username -- username
            password -- password
            first_name -- (optinal) first name
            last_name -- (optinal) last name
            email -- (optinal) email
            jwt_params -- (optinal) jwt params to get the lti information from
                user_id -- id of the user
                user_image -- user image
                roles -- role of the user

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when username or password is not set
            bad request -- when email/username/lti id already exists
            bad request -- when email/password is invalid
        On succes:
            success -- with the course data
        """
        if 'jwt_params' in request.data and request.data['jwt_params'] != '':
            lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
            user_id, user_image = utils.optional_params(lti_params, 'user_id', 'user_image')
            is_teacher = json.load(open('config.json'))['Teacher'] in lti_params['roles']
        else:
            user_id, user_image, is_teacher = None, None, False

        try:
            username, password = utils.required_params(request.data, 'username', 'password')
            first_name, last_name, email = utils.optional_params(request.data, 'first_name', 'last_name', 'email')
        except KeyError:
            return response.keyerror('username', 'password')

        if email and User.objects.filter(email=email).exists():
            return response.bad_request('User with this email address already exists.')
            try:
                validate_email(email)
            except ValidationError:
                return response.bad_request('Invalid email address.')

        if User.objects.filter(username=username).exists():
            return response.bad_request('User with this username already exists.')

        if user_id is not None and User.objects.filter(lti_id=user_id).exists():
            return response.bad_request('User with this lti id already exists.')

        if validate_password(password):
            return response.bad_request(validate_password(password))

        user = factory.make_user(username, password, email=email, lti_id=user_id, is_teacher=is_teacher,
                                 first_name=first_name, last_name=last_name, profile_picture=user_image)

        return response.created(self.serializer_class(user).data, obj='user')

    def partial_update(self, request, *args, **kwargs):
        """Update an existing user.

        Arguments:
        request -- request data
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
        if not request.user.is_authenticated:
            return response.unauthorized()
        pk = kwargs.get('pk')
        if request.user.pk is not int(pk) or not request.user.is_superuser:
            return response.forbidden()

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return request.not_found('user')

        serializer = OwnUserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()
        return response.success(serializer.data)

    def destroy(self, request, pk):
        """Delete a user.

        Arguments:
        request -- request data
        pk -- user ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the user does not exists
        On success:
            success -- deleted message
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if request.user.pk is not pk or not request.user.is_auperuser:
            return response.forbidden()

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return response.not_found('user')

        user.delete()
        return response.deleted('user')

    @action(methods=['patch'], detail=True)
    def change_password(self, request, pk):
        """Change the password of a user.

        Arguments:
        request -- request data
            new_password -- new password of the user
            old_password -- current password of the user
        pk -- user ID

        Returns
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when new or old password is not set
            bad request -- when the password is invalid
        On success:
            success -- with a success description
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        try:
            new_password, old_password = utils.required_params(request.data, 'new_password', 'old_password')
        except KeyError:
            return response.KeyError('new_password', 'old_password')

        if not request.user.is_authenticated or not request.user.check_password(old_password):
            return response.unauthorized('Wrong password.')

        if validate_password(new_password):
            return response.bad_request(validate_password(new_password))

        request.user.set_password(new_password)
        request.user.save()
        return response.success({}, description='Succesfully changed the password.')
