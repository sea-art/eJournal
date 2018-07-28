"""
responses.py.

This file contains functions to easily generate common HTTP error responses
using JsonResponses. These functions should be used whenever the client needs
to receive the appropriate error code.
"""
from django.http import JsonResponse

from django.http import FileResponse
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
from VLE.settings.base import *
import os
import magic


def success(message='success', payload={}):
    """Return a success response header.

    Arguments:
    payload -- payload to deliver on success
    """
    return response(200, message, payload=payload)


def created(message='success', payload={}):
    """Return a created response header.

    Arguments:
    payload -- payload to deliver after creation
    """
    return response(201, message, payload=payload)


def no_content(description='Request succeeded.'):
    """Return a no content header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(204, 'No Content', description=description)


def bad_request(description='Your browser performed a bad request.'):
    """Return a bad request response header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(400, 'Bad Request', description=description)


def unauthorized(description='You are not authenticated.'):
    """Return an unauthorized response header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(401, 'Authentication Error', description=description)


def forbidden(description='You have no access to this page'):
    """Return a forbidden response header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(403, 'Forbidden', description=description)


def not_found(description='The page or file you requested was not found.'):
    """Return a not found response header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(404, 'Not Found', description='{} not found.'.format(description))


def internal_server_error(description='Oops! The server experienced internal hiccups.'):
    """Return an internal server error response header.

    Arguments:
    description -- header description (usable for example in the front end)
    """
    return response(500, '500 Internal Server Error', description=description)


def response(status, message, description='', payload={}):
    """Return a generic response header with customizable fields.

    Arguments:
    status -- HTTP status number
    message -- response message
    description -- header description (usable for example in the front end)
    payload -- payload to deliver
    """
    return JsonResponse({'result': message, 'description': description, **payload}, status=status)


def keyerror(*keys):
    """Generate a bad request response when the input JSON has keyerror(s)."""
    if len(keys) == 1:
        return bad_request('Field {0} is required but is missing.'.format(keys))
    else:
        return bad_request('Fields {0} are required but one or more are missing.'.format(keys))


def file_response(relative_file_path):
    file_path = os.path.join(MEDIA_ROOT, relative_file_path)
    response = FileResponse(open(file_path, 'rb'))

    print(response)
    return response


def file_attachment(file_name, relative_file_path):
    file_path = os.path.join(MEDIA_ROOT, relative_file_path)
    FilePointer = open(file_path, "rb")
    response = HttpResponse(FilePointer, content_type=magic.from_file(file_path, mime=True))
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)

    return response


def download_file(relative_file_path):
    file_path = os.path.join(MEDIA_ROOT, relative_file_path)
    filename = os.path.basename(file_path)
    chunk_size = 8192
    response = StreamingHttpResponse(FileWrapper(open(file_path, 'rb'), chunk_size),
                                     content_type=magic.from_file(file_path, mime=True))
    response['Content-Length'] = os.path.getsize(file_path)
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    return response
