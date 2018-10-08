import VLE.views.responses as response
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from smtplib import SMTPAuthenticationError


class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            return response.not_found(f'{str(exception).split()[0]} does not exist.')
        elif isinstance(exception, ValidationError):
            return response.bad_request(exception.args[0])
        elif isinstance(exception, KeyError):
            return response.key_error(str(exception))
        elif isinstance(exception, ValueError):
            return response.value_error(str(exception))
        elif isinstance(exception, SMTPAuthenticationError):
            return response.internal_server_error(
                description='Mailserver is not configured correctly, please contact a server admin.')
