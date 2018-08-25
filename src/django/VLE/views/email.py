"""
email.py.

In this file are all the email api requests.
This includes:
    /forgot_password/ -- to get the names belonging to the ids
"""
from rest_framework.decorators import api_view
import VLE.views.responses as response
from VLE.models import User
import VLE.utils.email_handling as email_handling
import VLE.utils.generic_utils as utils
import VLE.validators as validators
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import PasswordResetTokenGenerator


@api_view(['POST'])
def forgot_password(request):
    """Handles a forgot password request.

    Arguments:
        username -- User claimed username
        email -- User claimed email
        token -- Django stateless token, invalidated after password change or after a set time (by default three days).

    Generates a recovery token if a matching user can be found by either the prodived username or email.
    """
    user = None

    try:
        utils.required_params(request.data, 'username', 'email')
    except KeyError:
        return response.KeyError('username', 'email')

    # We are retrieving the username based on either the username or email
    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        pass
    try:
        user = User.objects.get(email=request.data['email'])
    except User.DoesNotExist:
        pass

    if not user:
        return response.bad_request('No user found with that username or email.')

    email_handling.send_password_recovery_link(user)

    return response.success(description='An email was sent to %s, please follow the email for instructions.'
                            % user.email)


@api_view(['POST'])
def recover_password(request):
    """Handles a reset password request.

    Arguments:
        username -- User claimed username
        recovery_token -- Django stateless token, invalidated after password change or after a set time
            (by default three days).
        new_password -- The new user desired password

    Updates password if the recovery_token is valid.
    """
    try:
        utils.required_params(request.data, 'username', 'recovery_token', 'new_password')
    except KeyError:
        return response.KeyError('username', 'recovery_token', 'new_password')

    try:
        user = User.objects.get(username=request.data['username'])
    except User.DoesNotExist:
        return response.not_found('The username is unkown.')

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, request.data['recovery_token']):
        return response.bad_request('Invalid recovery token.')

    try:
        validators.validate_password(request.data['new_password'])
    except ValidationError as e:
        return response.bad_request(e.args[0])

    user.set_password(request.data['new_password'])
    user.save()

    return response.success(description='Succesfully changed the password, please login.')


@api_view(['POST'])
def verify_email(request):
    """Handles an email verification request.

    Arguments:
        token -- User claimed email verification token.

    Updates the email verification status.
    """
    user = request.user
    if not user.is_authenticated:
        return response.unauthorized()

    if user.verified_email:
        return response.success(description='Email address already verified.')

    try:
        utils.required_params(request.data, 'token')
    except KeyError:
        return response.KeyError('token')

    token_generator = PasswordResetTokenGenerator()
    if not token_generator.check_token(user, request.data['token']):
        return response.bad_request(description='Invalid email recovery token.')

    user.verify_email = True
    user.save()
    return response.success(description='Succesfully verified your email address.')


@api_view(['POST'])
def request_email_verification(request):
    """Request an email with a verifcation link for the users email address."""
    user = request.user
    if not user.is_authenticated:
        return response.unauthorized()

    if user.verified_email:
        return response.bad_request(description='Email address already verified.')

    email_handling.send_email_verification_link(user)

    return response.success(description='An email was sent to %s, please follow the email for instructions.'
                            % user.email)
