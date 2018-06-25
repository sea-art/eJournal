"""
test_apis.py.

Test API calls.
"""
from django.test import TestCase

import VLE.factory as factory

import test.test_rest as test


class ApiTests(TestCase):
    """Api tests.

    Test api calls.
    """

    def setUp(self):
        """Setup."""
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_get_course_users(self):
        """Test get courses of user."""
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        rein = factory.make_user("Rein", "123")
        lars = factory.make_user("Lars", "123")

        TA = factory.make_role("TA")
        SD = factory.make_role("SD")
        factory.make_participation(rein, course, TA)
        factory.make_participation(lars, course, SD)

        response = test.api_get_call(self, '/api/get_course_users/' + str(course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 2)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

    def test_create_entry(self):
        """"Test create entry."""
        login = test.logging_in(self, self.username, self.password)

        assignment = factory.make_assignment("Assignment", "Your favorite assignment")
        journal = factory.make_journal(assignment, self.user)
        template = factory.make_entry_template("some_template")
        field = factory.make_field(template, 'Some field', 0)

        some_dict = {
            'jID': journal.id,
            'tID': template.id,
            'content': [{
                'tag': field.pk,
                'data': "This is some data"
                }]
            }

        test.api_post_call(self, '/api/create_entry/', some_dict, login, 201)
