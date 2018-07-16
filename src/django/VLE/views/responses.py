"""
responses.py.

This file contains functions to easily generate common HTTP error responses
using JsonResponses. These functions should be used whenever the client needs
to receive the appropriate error code.
"""
from rest_framework.response import Response


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
    return Response({'result': message, 'description': description, **payload}, status=status)


def keyerror(*keys):
    """Generate a bad request response when the input JSON has keyerror(s)."""
    if len(keys) == 1:
        return bad_request('Field {0} is required but is missing.'.format(keys))
    else:
        return bad_request('Fields {0} are required but one or more are missing.'.format(keys))
