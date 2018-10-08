import VLE.views.responses as response
from django.core.exceptions import ObjectDoesNotExist
import re


class ErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            DoesNotExist = re.search(
                r'([A-z .]*)matching query does not exist([A-z .]*[\']+)',
                getattr(exception, 'message', repr(exception)))
            return response.not_found(f'{DoesNotExist.group(1)} does not exist.')
