"""
test_authentication.py.

Test the authentication calls.
"""

from django.test import TestCase
from django.urls import reverse


import VLE.factory as factory
import test.test_utils as test


class AuthenticationTests(TestCase):
    """Test django rest authentication calls.

    Test the authentication api calls
    """
    def setUp(self):
        """Set up the test file."""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')

    def test_login(self):
        """Test if the login is successful."""
        login = test.logging_in(self, self.username, self.password)
        factory.make_course('test', 'TTTT')
        test.api_get_call(self, '/api/get_user_courses/', login)

    def test_not_logged_in(self):
        """Test error for api request call for non-authenticated user."""
        result = self.client.get(reverse('get_user_courses'), {}, format='json')
        self.assertEquals(result.status_code, 401)
