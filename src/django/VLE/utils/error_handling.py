from smtplib import SMTPAuthenticationError

from django.core.exceptions import ObjectDoesNotExist, ValidationError

import VLE.views.responses as response


class VLEMissingRequiredKey(KeyError):
    pass


class VLEParamWrongType(ValueError):
    pass


class VLEProgrammingError(Exception):
    pass


class VLEPermissionError(Exception):
    def __init__(self, permission=None, message=None):
        if message:
            super(VLEPermissionError, self).__init__(message)
        else:
            super(VLEPermissionError, self).__init__('User does not have permission ' + permission)


class VLEParticipationError(Exception):
    def __init__(self, obj):
        super(VLEParticipationError, self).__init__('User is not participating in ' + str(obj))


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
                'Mailserver is not configured correctly, please contact a server admin.')
        elif isinstance(exception, VLEProgrammingError):
            return response.internal_server_error(str(exception))
        elif isinstance(exception, VLEParticipationError):
            return response.forbidden(str(exception))
        elif isinstance(exception, VLEPermissionError):
            return response.forbidden(str(exception))
