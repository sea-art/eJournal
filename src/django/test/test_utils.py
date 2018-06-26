"""
test_utils.py.

Test helper functions.
"""

from django.urls import reverse
import json


import VLE.factory as factory


def set_up_user_and_auth(username, password):
    """Sets up a teacher user.

    Arguments:
    username -- username for the user
    password -- password for the user

    Returns the user and its credentials
    """
    user = factory.make_user(username, password)
    return username, password, user


def set_up_users(name, n):
    """Sets up some students.

    Arguments:
    name -- the base for the incremental name
    n -- number of students to be made

    Returns a list of users with incremental naming.
    """
    users = []
    for i in range(n):
        users.append(factory.make_user(name + str(i), 'pass'))
    return users


def set_up_entries(template, n):
    """Sets up some entries.

    Arguments:
    template -- the template to be used for the entries
    n -- number of entriest to be made

    Returns a list of entries that uses the same template.
    """
    entries = []
    for i in range(n):
        entries.append(factory.make_entry(template))
    return entries


def logging_in(obj, username, password, status=200):
    """Login using username and password.

    Arguments:
    username -- username
    password -- password
    status -- status it checks for after login (default 200)

    Returns the loggin in user.
    """
    result = obj.client.post(reverse('token_obtain_pair'),
                             json.dumps({'username': username, 'password': password}),
                             content_type='application/json')
    obj.assertEquals(result.status_code, status)
    return result


def api_get_call(obj, url, login, status=200):
    """Send an get api call.

    Arguments:
    url -- url to send the call to
    login -- credentials of the logged in user
    status -- status it checks for after login (default 200)

    returns the whatever the api call returns
    """
    result = obj.client.get(url, {},
                            HTTP_AUTHORIZATION='Bearer {0}'.format(login.data['access']))
    obj.assertEquals(result.status_code, status)
    return result


def api_post_call(obj, url, params, login, status=200):
    """Send an get api call.

    Arguments:
    url -- url to send the call to
    params -- extra parameters that the api needs
    login -- credentials of the logged in user
    status -- status it checks for after login (default 200)

    returns the whatever the api call returns
    """
    result = obj.client.post(url, json.dumps(params), content_type='application/json',
                             HTTP_AUTHORIZATION='Bearer {0}'.format(login.data['access']))
    obj.assertEquals(result.status_code, status)
    return result
