from django.test import TestCase

import VLE.factory as factory

import test.test_utils as test


class GetApiTests(TestCase):
    def setUp(self):
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')

        self.course = factory.make_course("Beeldbewerken", "BB")

        self.rein = factory.make_user("Rein", "123")
        self.lars = factory.make_user("Lars", "123")

    def test_get_own_user_data(self):
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_own_user_data/', login)

        self.assertEquals(response.json()['user']['name'], self.username)

    def test_course_data(self):
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_course_data/' + str(self.course.pk) + '/', login)

        self.assertEquals(response.json()['course']['name'], 'Beeldbewerken')
        self.assertEquals(response.json()['course']['abbr'], 'BB')

    def test_get_course_users(self):
        login = test.logging_in(self, self.username, self.password)

        TA = factory.make_role("TA", self.course)
        SD = factory.make_role("SD", self.course)
        factory.make_participation(self.rein, self.course, TA)
        factory.make_participation(self.lars, self.course, SD)

        response = test.api_get_call(self, '/api/get_course_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 2)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

    def test_get_unenrolled_users(self):
        login = test.logging_in(self, self.username, self.password)

        TA = factory.make_role("TA", self.course)
        SD = factory.make_role("SD", self.course)
        factory.make_participation(self.rein, self.course, TA)
        factory.make_participation(self.lars, self.course, SD)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

    def test_get_course_roles(self):
        """Test the get delete assignment function."""
        teacher_user = 'Teacher'
        teacher_pass = 'pass'
        teacher = factory.make_user(teacher_user, teacher_pass)
        factory.make_role("TA", self.course)
        factory.make_role("SD", self.course)
        factory.make_role("HE", self.course)
        teacher_role = factory.make_role_all_permissions("TE", self.course)
        factory.make_participation(teacher, self.course, teacher_role)
        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_get_call(self, '/api/get_course_roles/1/', login)
        self.assertEquals(len(result.json()['roles']), 4)
