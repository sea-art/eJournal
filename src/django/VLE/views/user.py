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
from VLE.models import User, Journal, UserFile, Assignment
from VLE.views import responses as response
import VLE.utils.generic_utils as utils
import VLE.factory as factory
from VLE.utils import email_handling
from VLE.utils import file_handling
import VLE.validators as validators
import VLE.permissions as permissions

import jwt
import json


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
        return response.success({'users': serializer.data})

    def retrieve(self, request, pk):
        """Get the user data of the given user.

        Arguments:
        request -- request data
        pk -- user ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the user doesn't exists
        On success:
            success -- with the user data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        if int(pk) is 0:
            pk = request.user.id

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return response.not_found('user')

        if request.user == user or request.user.is_superuser:
            serializer = OwnUserSerializer(user, many=False)
        else:
            serializer = self.serializer_class(user, many=False)
        return response.success({'user': serializer.data})

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
            success -- with the newly created user data
        """
        if 'jwt_params' in request.data and request.data['jwt_params'] != '':
            lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
            lti_id, user_image = utils.optional_params(lti_params, 'user_id', 'user_image')
            is_teacher = json.load(open('config.json'))['Teacher'] in lti_params['roles']
        else:
            lti_id, user_image, is_teacher = None, None, False

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

        if lti_id is not None and User.objects.filter(lti_id=lti_id).exists():
            return response.bad_request('User with this lti id already exists.')

        try:
            validators.validate_password(password)
        except ValidationError as e:
            return response.bad_request(e.args[0])

        user = factory.make_user(username, password, email=email, lti_id=lti_id, is_teacher=is_teacher,
                                 first_name=first_name, last_name=last_name, profile_picture=user_image)

        if lti_id is None:
            email_handling.send_email_verification_link(user)

        return response.created({'user': self.serializer_class(user).data})

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
        if not request.user.is_authenticated:
            return response.unauthorized()
        pk = kwargs.get('pk')
        if int(pk) is 0:
            pk = request.user.id
        if request.user.pk != int(pk) and not request.user.is_superuser:
            return response.forbidden()

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return request.not_found('user')

        if 'jwt_params' in request.data and request.data['jwt_params'] != '':
            lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
            lti_id, user_image = utils.optional_params(lti_params, 'user_id', 'custom_user_image')
            is_teacher = json.load(open('config.json'))['Teacher'] in lti_params['roles']
        else:
            lti_id, user_image, is_teacher = None, None, False
        if user_image is not None:
            user.profile_picture = user_image
        if is_teacher:
            user.is_teacher = is_teacher

        if lti_id:
            if User.objects.filter(lti_id=lti_id).exists() and User.objects.filter(lti_id=lti_id) is not user:
                return response.bad_request('User with this lti id already exists.')
            user.lti_id = lti_id

        user.save()

        serializer = OwnUserSerializer(user, data=request.data, partial=True)
        if not serializer.is_valid():
            return response.bad_request()
        serializer.save()
        return response.success({'user': serializer.data})

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
        if int(pk) is 0:
            pk = request.user.id

        if request.user.pk is not pk or not request.user.is_auperuser:
            return response.forbidden()

        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return response.not_found('user')

        user.delete()
        return response.deleted(description='Sucesfully deleted user.')

    @action(methods=['patch'], detail=False)
    def password(self, request):
        """Change the password of a user.

        Arguments:
        request -- request data
            new_password -- new password of the user
            old_password -- current password of the user

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

        if not request.user.check_password(old_password):
            return response.bad_request('Wrong password.')

        if validators.validate_password(new_password):
            return response.bad_request(validators.validate_password(new_password))

        request.user.set_password(new_password)
        request.user.save()
        return response.success(description='Succesfully changed the password.')

    # TODO: Fix this stuff
    # TODO: limit this request for end users, otherwise its really easy to DDOS the server.
    @action(methods=['get'], detail=True)
    def GDPR(self, request, pk):
        """Get a zip file of all the userdata.

        Arguments:
        request -- request data
        pk -- user ID to download the files from

        Returns
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- when its not a superuser nor their own data
        On success:
            success -- a zip file of all the userdata with all their files
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        if int(pk) is 0:
            pk = request.user.id

        user = User.objects.get(pk=pk)

        # Check the right permissions to get this users data, either be the user of the data or be an admin.
        permission = permissions.get_permissions(user, cID=-1)
        if not permission['is_superuser'] and request.user.id != pk:
            return response.forbidden('You cannot view this users data.')

        profile = UserSerializer(user).data
        journals = Journal.objects.filter(user=pk)
        journal_dict = {}
        # TODO: Add entry serializer
        for journal in journals:
            pass
            # Select the nodes of this journal but only the ones with entries.
            # nodes_of_journal_with_entries = Node.objects.filter(journal=journal).exclude(entry__isnull=True)
            # Serialize all entries and put them into the entries dictionary with the assignment name key.
            # entries_of_journal =[serialize.export_entry_to_dict(node.entry) for node in nodes_of_journal_with_entries]
            # journal_dict.update({journal.assignment.name: entries_of_journal})

        archive_path, content_type = file_handling.compress_all_user_data(
            user,
            {'profile': profile, 'journals': journal_dict}
        )

        return response.file_b64(archive_path, content_type)

    # TODO: check if it works
    @action(methods=['get'], detail=True)
    def download(self, request, pk):
        """Get a user file by name if it exists.

        Arguments:
        request -- the request that was sent
            file_name -- filename to download
        pk -- user ID

        Returns
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when file_name is not set
            bad_request -- when the file was not found
            forbidden -- when its not a superuser nor their own data
        On success:
            success -- a zip file of all the userdata with all their files
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        if int(pk) is 0:
            pk = request.user.id

        try:
            file_name, = utils.required_params(request.query_params, 'file_name')
        except KeyError:
            return response.KeyError('file_name')

        try:
            user_file = UserFile.objects.get(author=pk, file_name=file_name)
        except UserFile.DoesNotExist:
            return response.bad_request(file_name + ' was not found.')

        if user_file.author.id is not request.user.id and \
           not permissions.has_assignment_permission(
                request.user, user_file.assignment, 'can_view_assignment_participants'):
            return response.forbidden('Forbidden to view: %s by author ID: %s.' % (file_name, pk))

        return response.user_file_b64(user_file)

    # TODO: Check if it works
    @action(methods=['post'], detail=True)
    def upload(self, request, pk):
        """Update user profile picture.

        No validation is performed beyond a size check of the file and the available space for the user.

        Arguments:
        request -- request data
            file -- filelike data

        Returns
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when file is not set
            bad_request -- when the file was not found
        On success:
            success -- a zip file of all the userdata with all their files
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if not request.FILES or 'file' not in request.FILES or 'aID' not in request.POST:
            return response.bad_request()

        try:
            validators.validate_user_file(request.FILES['file'])
        except ValidationError:
            return response.bad_request('The selected file exceeds the file limit.')

        user_files = request.user.userfile_set.all()

        # Fast check for allowed user storage space
        if settings.USER_MAX_TOTAL_STORAGE_BYTES - len(user_files) * settings.USER_MAX_FILE_SIZE_BYTES <= \
           request.FILES['file'].size:
            # Slow check for allowed user storage space
            file_size_sum = 0
            for user_file in user_files:
                file_size_sum += user_file.file.size
            if file_size_sum > settings.USER_MAX_TOTAL_STORAGE_BYTES:
                return response.bad_request('Unsufficient user storage space.')

        # Ensure an old copy of the file is removed when updating a file with the same name.
        try:
            old_user_file = user_files.get(file_name=request.FILES['file'].name)
            old_user_file.file.delete()
            old_user_file.delete()
        except UserFile.DoesNotExist:
            pass

        try:
            assignment = Assignment.objects.get(pk=request.POST['aID'])
        except Journal.DoesNotExist:
            return response.bad_request('Journal with id {:s} was not found.'.format(request.POST['aID']))

        factory.make_user_file(request.FILES['file'], request.user, assignment)

        return response.success(description='Succesfully uploaded {:s}.'.format(request.FILES['file'].name))

    # TODO: check if it works
    @action(['post'], detail=False)
    def set_profile_picture(self, request):
        """Update user profile picture.

        Arguments:
        request -- request data
            file -- a base64 encoded image

        Returns
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when url_data is not set
            bad_request -- when the file is not valid
        On success:
            success -- a zip file of all the userdata with all their files
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            utils.required_params(request.data, 'file')
        except KeyError:
            return response.keyerror('file')

        try:
            validators.validate_profile_picture_base64(request.data['file'])
        except ValidationError:
            return response.bad_request('Profile picture did not pass validation!')

        request.user.profile_picture = request.data['file']
        request.user.save()

        return response.success(description='Succesfully updated profile picture')
