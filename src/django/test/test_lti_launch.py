"""
test_lti_launch.py.

Test lti launch.
"""
from django.test import TestCase, RequestFactory
from django.conf import settings
# from VLE.models import Journal, Lti_ids

import VLE.lti_launch as lti
import VLE.factory as factory
import VLE.views.lti as lti_view
import json
import oauth2
import time


class lti_launch_test(TestCase):
    """Lti lanch test.

    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        """Setup."""
        self.roles = json.load(open(settings.LTI_ROLE_CONFIG_PATH))
        self.factory = RequestFactory()

        self.request = {"oauth_consumer_key": settings.LTI_KEY,
                        "oauth_signature_method": "HMAC-SHA1",
                        "oauth_version": "1.0",
                        "custom_assignment_due": "2018-11-10 23:59:00 +0100",
                        "custom_assignment_id": "bughh",
                        "custom_assignment_lock": "2018-12-15 23:59:59 +0100",
                        "custom_assignment_title": "TestAss",
                        "custom_assignment_unlock": "2018-08-16 00:00:00 +0200",
                        "custom_assignment_points": "10",
                        "custom_course_id": "asdf",
                        "custom_course_name": "TestCourse",
                        "context_label": "aaaa",
                        "custom_user_email": "ltiTest@test.com",
                        "custom_user_full_name": "testpersoon voor Science",
                        "custom_username": "TestUser",
                        "lti_message_type": "basic-lti-launch-request",
                        "lti_version": "LTI-1p0",
                        "roles": "Instructor",
                        "user_id": "0000",
                        "oauth_signature": "sxmVoGtVMxAVseeqTh8bc0ZFue8="}

        self.oauth_consumer = oauth2.Consumer(
            settings.LTI_KEY, settings.LTI_SECRET
        )

        self.created_user = factory.make_user('TestUser', 'Pass', "ltiTest@test.com", lti_id='awefd')

    def test_select_user(self):
        """Hopefully select a user."""
        selected_user = lti.check_user_lti({
            'user_id': self.created_user.lti_id
        }, self.roles)
        self.assertEquals(selected_user, self.created_user)

    def test_lti_launch_no_user(self):
        """ ."""
        self.request["oauth_timestamp"] = int(time.time())
        self.request["oauth_nonce"] = oauth2.generate_nonce()
        oauth_request = oauth2.Request.from_request(
            'POST', 'http://127.0.0.1:8000/lti/launch', parameters=self.request
        )
        oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, {})
        self.request['oauth_signature'] = oauth_request['oauth_signature'].decode('utf-8')
        request = self.factory.post('http://127.0.0.1:8000/lti/launch', self.request)
        response = lti_view.lti_launch(request)
        self.assertEquals(response.status_code, 302)
        self.assertIs('state={0}'.format(lti_view.NO_USER) in response.url, True)

    # def test_select_course(self):
    #     """Hopefully select a course."""
    #     selected_course = lti.check_course_lti({
    #         'custom_course_id': Lti_ids.objects.filter(course=self.created_course)[0].lti_id,
    #     },
    #         user=self.created_user,
    #         role=self.roles['Teacher']
    #     )
    #     self.assertEquals(selected_course, self.created_course)
    #
    # def test_select_assignment(self):
    #     """Hopefully select a assignment."""
    #     selected_assignment = lti.check_assignment_lti({
    #         'custom_assignment_id': Lti_ids.objects.filter(assignment=self.created_assignment)[0].lti_id,
    #     })
    #     self.assertEquals(selected_assignment, self.created_assignment)
    #
    # def test_select_journal(self):
    #     """Hopefully select a journal."""
    #     selected_journal = lti.select_create_journal({
    #         'roles': self.roles['Student'],
    #     },
    #         user=self.created_user,
    #         assignment=self.created_assignment,
    #         roles=self.roles
    #     )
    #     self.assertEquals(selected_journal, self.created_journal)
    #
    # def test_create_journal(self):
    #     """Hopefully create a journal."""
    #     self.created_journal.delete()
    #     selected_journal = lti.select_create_journal({
    #         'roles': self.roles['Student'],
    #     },
    #         user=self.created_user,
    #         assignment=self.created_assignment,
    #         roles=self.roles
    #     )
    #     self.assertIsInstance(selected_journal, Journal)
    #
    # def test_create_journal_unauthorized(self):
    #     """Only a teacher should be able to create journal if non can be selected."""
    #     selected_journal = lti.select_create_journal({
    #         'roles': self.roles['TA'],
    #     },
    #         user=self.created_user,
    #         assignment=self.created_assignment,
    #         roles=self.roles
    #     )
    #     self.assertEquals(None, selected_journal)
