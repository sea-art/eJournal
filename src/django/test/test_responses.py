"""
test_responses.py

This file tests whether all HTTP responses behave as required.
"""
from django.test import TestCase

import VLE.views.responses as responses
from django.http import JsonResponse


class ResponsesTests(TestCase):
    """Test the responses system.

    Test whether the HTTP responses behave as required.
    """

    def test_response_type(self):
        """Test whether the response type is correct."""
        response = responses.bad_request()

        self.assertTrue(isinstance(response, JsonResponse))
