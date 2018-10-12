from smtplib import SMTPAuthenticationError

from django.core.exceptions import ObjectDoesNotExist, ValidationError

import VLE.views.responses as response


class VLEMissingRequiredKey(KeyError):
    pass


class VLEParamWrongType(ValueError):
    pass


class VLEProgrammingError(Exception):
    pass


class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            return response.not_found('{0} does not exist.'.format(str(exception).split()[0]))
        elif isinstance(exception, ValidationError):
            return response.bad_request(exception.args[0])
        elif isinstance(exception, VLEMissingRequiredKey):
            return response.key_error(str(exception))
        elif isinstance(exception, VLEParamWrongType):
            return response.value_error(str(exception))
        elif isinstance(exception, SMTPAuthenticationError):
            return response.internal_server_error(
                description='Mailserver is not configured correctly, please contact a server admin.')
