from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage


def send_email_verification_link(user):
    """Sends an email verification link to the users email adress."""
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)

    recovery_link = '%s/EmailVerification/%s' % (settings.BASELINK, token)
    email_body = '''\
We have received a request for email verification, if you have not made this request please ignore this email.
If you did make the request please visit the link below to verify your email address:

{recovery_link}

Or copy the token manually: {token}\
'''.format(recovery_link=recovery_link, token=token)

    print('woosh')
    EmailMessage('eJourn.al email verification', email_body, to=[user.email]).send()


def send_password_recovery_link(user):
    """Sends an email verification link to the users email address.."""
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)

    recovery_link = '%s/PasswordRecovery/%s/%s' % (settings.BASELINK, user.username, token)
    email_body = '''\
We have received a request for password recovery, if you have not made this request please ignore this email.
If you did make the request please visit the link below and set a new password:

{recovery_link}\
'''.format(recovery_link=recovery_link)

    EmailMessage('eJourn.al password recovery', email_body, to=[user.email]).send()
