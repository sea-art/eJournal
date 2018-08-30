# """
# assignment.py.
#
# Test the assignment view calls.
# """
#
# from django.test import TestCase
# from django.test import Client
#
# from django.test import TestCase
#
# import VLE.factory as factory
#
# import test.test_utils as test
# from VLE.models import Assignment
#
#
# class AssignmentViewTests(TestCase):
#     """Test django rest assignment calls.
#
#     Test the assignment api calls
#     """
#     def setUp(self):
#         """Set up the test file."""
#         self.c = Client()
#
#     def test_list(self):
#         response = self.c.post('/assignments/')
#         self.assertEquals(response.status, 200)
