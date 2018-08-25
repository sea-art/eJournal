"""
responses.py.

This file contains functions to easily generate common HTTP error responses
using JsonResponses. These functions should be used whenever the client needs
to receive the appropriate error code.
"""
from django.http import JsonResponse, HttpResponse, FileResponse

import os
from VLE.settings.base import MEDIA_ROOT
import base64


def success(payload={}, description=''):
    """Calls a json_response with status 200: Ok.

    Arguments:
        payload      -- Data to send with the request, should be dict instance.
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Ok'.
    """
    return json_response(payload=payload, description=description, status=200)


def created(payload={}, description=''):
    """Calls a json_response with status 201: Created.

    Arguments:
        payload      -- Data to send with the request, should be dict instance.
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Created'.
    """
    return json_response(payload=payload, description=description, status=201)


def bad_request(description='Your browser performed a bad request.'):
    """Calls a json_response with status 400: Bad Request.

    Arguments:
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Bad Request'.
    """
    return json_response(description=description, status=400)


def unauthorized(description='You are not authenticated.'):
    """Calls a json_response with status 401: Unauthorized.

    Arguments:
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Unauthorized'.
    """
    return json_response(description=description, status=401)


def forbidden(description='You have no access to this page'):
    """Calls a json_response with status 403: Forbidden.

    Arguments:
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Forbidden'.
    """
    return json_response(description=description, status=403)


def not_found(description='The page or file you requested was not found.'):
    """Calls a json_response with status 404: Not Found.

    Arguments:
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Not Found'.
    """
    return json_response(description=description, status=404)


def internal_server_error(description='Oops! The server experienced internal hiccups.'):
    """Calls a json_response with status 500: Internal Server Error.

    Arguments:
        description  -- Additional information about the reason of the response, included in the data payload.
                        This serves in addition to the HTTP default reason phrase 'Internal Server Error'.
    """
    return json_response(description=description, status=500)


def response(status, message, description='', payload={}):
    """Return a generic response header with customizable fields.

    Arguments:
    status -- HTTP status number
    message -- response message
    description -- header description (usable for example in the front end)
    payload -- payload to deliver
    """
    return JsonResponse({'result': message, 'description': description, **payload}, status=status)


def http_response(content=b'', content_type=None, status=None, reason=None, charset=None):
    """Returns a HttpResponse.

    Arguments:
    content      -- Data to send with the request, should be byte string.
    content_type -- Sets the HTTP MIMI type of the request body.
                    Default: django.conf settings.DEFAULT_CHARSET = text/html
    status       -- HTTP status code for the response.
    reason       -- HTTP response phrase. If not provided, a default phrase will be used. Keyed as statusText.
    charset      -- A string denoting the charset in which the response will be encodedself.
                    Default: django.conf settings.DEFAULT_CHARSET = utf-8

    Additional headers can be set by treating the response as a dictionary.
    """
    return HttpResponse(content=content, content_type=content_type, status=status, reason=reason, charset=None)


def json_response(payload={}, description='', status=None, reason=None, charset=None):
    """Returns a JsonResponse with HTTP Content-Type header: Application/json.

    Arguments:
    payload      -- Data to send with the request, should be dict instance.
                    Will be serialized by DjangoJSONencoder by default. Keyed as data.
    description  -- Additional information about the reason of the response, included in the data payload.
    status       -- HTTP status code for the response.
    reason       -- HTTP response phrase. If not provided, a default phrase will be used. Keyed as statusText.
    charset      -- A string denoting the charset in which the response will be encodedself.
                    Default: django.conf settings.DEFAULT_CHARSET = utf-8
    """
    return JsonResponse(data={**payload, 'description': description}, status=status, reason=reason, charset=None)


def keyerror(*keys):
    """Generate a bad request response with each given key formatted in the description."""
    if len(keys) == 1:
        return bad_request(description='Field {0} is required but is missing.'.format(keys))
    else:
        return bad_request(description='Fields {0} are required but one or more are missing.'.format(keys))


def user_file_b64(user_file):
    """Return a file as base64 encoded binary string if found, otherwise returns a not found response."""
    file_path = os.path.join(MEDIA_ROOT, user_file.file.name)
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fp:
            response = HttpResponse(base64.b64encode(fp.read()), content_type=user_file.content_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            # Exposes headers to the response in javascript lowercase recommended
            response['access-control-expose-headers'] = 'content-disposition, content-type'
            return response
    else:
        return not_found(description='File not found.')


def file_b64(file_path, content_type):
    """Return a file as base64 encoded binary string if found, otherwise returns a not found response."""
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fp:
            response = HttpResponse(base64.b64encode(fp.read()), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            # Exposes headers to the response in javascript lowercase recommended
            response['access-control-expose-headers'] = 'content-disposition, content-type'
            return response
    else:
        return not_found(description='File not found.')


def file(file_path):
    """Return a file as bytestring if found, otherwise returns a not found response."""
    try:
        response = FileResponse(open(file_path, 'rb'), as_attachment=True)
        return response
    except FileNotFoundError:
        return not_found(description='File not found.')
