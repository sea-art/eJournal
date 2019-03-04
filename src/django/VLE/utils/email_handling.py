from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from VLE.models import Role


def send_email_verification_link(user):
    """Sends an email verification link to the users email adress."""
    email_data = {}
    email_data['heading'] = 'Email verification'
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    email_data['main_content'] = '''\
    We have received a request for email verification. If it was you who made this request, \
    please click the button below to verify your email address. If you have not made this \
    request please ignore this email.'''
    email_data['extra_content'] = 'Token: {}'.format(token)
    email_data['button_url'] = '{}/EmailVerification/{}/{}'.format(settings.BASELINK, user.username, token)
    email_data['button_text'] = 'Verify Email'
    email_data['profile_url'] = '{}/Profile'.format(settings.BASELINK)

    html_content = render_to_string('call_to_action.html', {'email_data': email_data})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='eJournal email verification',
        body=text_content,
        from_email='noreply@ejourn.al',
        headers={'Content-Type': 'text/plain'},
        to=[user.email]
    )

    email.attach_alternative(html_content, 'text/html')
    email.send()


def send_password_recovery_link(user):
    """Sends an email verification link to the users email address.."""
    email_data = {}
    email_data['heading'] = 'Password recovery'
    token_generator = PasswordResetTokenGenerator()
    token = token_generator.make_token(user)
    email_data['main_content'] = '''\
    We have received a request for password recovery. If it was you who made this request, \
    please click the button below to set a new password. If you have not made this \
    request please ignore this email.'''
    email_data['extra_content'] = 'Token: {}'.format(token)
    email_data['button_url'] = '{}/PasswordRecovery/{}/{}'.format(settings.BASELINK, user.username, token)
    email_data['button_text'] = 'Set New Password'
    email_data['profile_url'] = '{}/Profile'.format(settings.BASELINK)

    html_content = render_to_string('call_to_action.html', {'email_data': email_data})
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject='eJournal password recovery',
        body=text_content,
        from_email='noreply@ejourn.al',
        headers={'Content-Type': 'text/plain'},
        to=[user.email]
    )

    email.attach_alternative(html_content, 'text/html')
    email.send()


def send_email_feedback(user, topic, ftype, feedback, user_agent, url, files=[]):
    """Sends the feedback of an user to the developers."""
    f_body = 'TYPE: {}\n\n'.format(ftype[0])
    f_body += 'FEEDBACK BY: {}\n'.format(user.username)
    f_body += 'EMAIL: {}\n'.format(user.email)
    f_body += 'TEACHER: {}\n'.format(user.is_teacher)
    f_body += 'ROLES: {}\n'.format(Role.objects.filter(role__user=user).values('name'))
    f_body += 'USER-AGENT: {}\n'.format(user_agent[0])
    f_body += 'URL: {}\n\n'.format(url[0])
    f_body += 'THE FEEDBACK:\n{}'.format(feedback[0])

    r_email_data = {}
    r_email_data['feedback'] = feedback[0]
    if len(files) > 0:
        r_email_data['attachments_added'] = True
    r_email_data['profile_url'] = '{}/Profile'.format(settings.BASELINK)

    r_html_content = render_to_string('feedback.html', {'email_data': r_email_data})
    r_text_content = strip_tags(r_html_content)

    attachments = []
    for file in files:
        attachments.append((file.name, file.read(), file.content_type))

    reply = EmailMultiAlternatives(
        subject='Thank you for your feedback!',
        body=r_text_content,
        attachments=attachments,
        from_email='support@ejourn.al',
        headers={'Content-Type': 'text/plain'},
        to=[user.email]
    )

    forward = EmailMultiAlternatives(
        subject='[Feedback] {}'.format(topic[0]),
        body=f_body,
        attachments=attachments,
        from_email='support@ejourn.al',
        to=['support@ejourn.al'],
        headers={'Content-Type': 'text/plain'},
        reply_to=[user.email]
    )

    reply.attach_alternative(r_html_content, 'text/html')
    reply.send()
    forward.send()
