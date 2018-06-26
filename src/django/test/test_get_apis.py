from django.test import TestCase

import VLE.factory as factory

import test.test_rest as test


class GetApiTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_get_own_user_data(self):
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_own_user_data/', login)

        self.assertEquals(response.json()['user']['name'], self.username)

    def test_course_data(self):
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        response = test.api_get_call(self, '/api/get_course_data/' + str(course.pk) + '/', login)

        self.assertEquals(response.json()['course']['name'], 'Beeldbewerken')
        self.assertEquals(response.json()['course']['abbr'], 'BB')

    def test_get_course_users(self):
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

    def test_get_unenrolled_users(self):
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        rein = factory.make_user("Rein", "123")
        lars = factory.make_user("Lars", "123")

        TA = factory.make_role("TA")
        SD = factory.make_role("SD")
        factory.make_participation(rein, course, TA)
        factory.make_participation(lars, course, SD)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)
