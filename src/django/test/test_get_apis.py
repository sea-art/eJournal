from django.test import TestCase

import VLE.factory as factory

import test.test_utils as test


class GetApiTests(TestCase):
    def setUp(self):
        """Set up the test file."""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')
        self.rein_user, self.rein_pass, self.rein = test.set_up_user_and_auth("Rein", "123")

        self.course = factory.make_course("Beeldbewerken", "BB")

        self.lars = factory.make_user("Lars", "123")

    def test_get_own_user_data(self):
        """Tests the get own user data function."""
        login = test.logging_in(self, self.username, self.password)
        response = test.api_get_call(self, '/api/get_own_user_data/', login)

        self.assertEquals(response.json()['user']['name'], self.username)

        test.unauthorized_api_get_call_test(self,  '/api/get_own_user_data/')

    def test_get_course_data(self):
        """Tests get coursedata function."""
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_course_data/' + str(self.course.pk) + '/', login)

        self.assertEquals(response.json()['course']['name'], 'Beeldbewerken')
        self.assertEquals(response.json()['course']['abbr'], 'BB')

        test.unauthorized_api_get_call_test(self, '/api/get_course_data/' + str(self.course.pk) + '/')

    def test_get_course_users(self):
        """Test the get course users function."""
        teacher = factory.make_user('Teacher', 'pass')
        TE = factory.make_role_teacher("TE", self.course)
        factory.make_participation(teacher, self.course, TE)

        login = test.logging_in(self, 'Teacher', 'pass')
        TA = factory.make_role_ta("TA", self.course)
        SD = factory.make_role_student("SD", self.course)
        factory.make_participation(self.rein, self.course, TA)
        factory.make_participation(self.lars, self.course, SD)

        response = test.api_get_call(self, '/api/get_course_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 3)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

        test.unauthorized_api_get_call_test(self,  '/api/get_course_users/' + str(self.course.pk) + '/')
        test.unauthorized_api_get_call_test(self, '/api/get_unenrolled_users/' + str(self.course.pk) + '/')

    def test_get_unenrolled_users(self):
        """Test the get get_unenrolledusers."""
        login = test.logging_in(self, self.username, self.password)

        TA = factory.make_role_ta("TA", self.course)
        SD = factory.make_role_student("SD", self.course)
        factory.make_participation(self.rein, self.course, TA)
        factory.make_participation(self.lars, self.course, SD)

        response = test.api_get_call(self, '/api/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 1)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

        test.unauthorized_api_get_call_test(self, '/api/get_unenrolled_users/')

    def test_get_user_courses(self):
        """Test the get user courses function."""
        for course in test.set_up_courses('course', 4):
            student_role = factory.make_role_student('Student', course)
            factory.make_participation(self.user, course, student_role)

        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_user_courses/', login)
        self.assertEquals(len(response.json()['courses']), 4)

        test.unauthorized_api_get_call_test(self, '/api/get_user_courses/')

    def test_get_linkable_courses(self):
        """Test the get linkable courses function."""
        test.set_up_courses('course', 3, author=self.user)
        test.set_up_courses('course', 4, author=self.user, lti_id=True)

        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_linkable_courses/', login)
        self.assertEquals(len(response.json()['courses']), 3)

        test.unauthorized_api_get_call_test(self, '/api/get_linkable_courses/')

    def test_get_course_assignment(self):
        """Test the get course assignment function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        assigns = test.set_up_assignments('assign', 'desc', 2, course=course)
        student_role = factory.make_role_student('Student', course)
        factory.make_participation(self.user, course, student_role)
        factory.make_journal(assigns[0], self.user)
        factory.make_journal(assigns[1], self.user)

        login_user = test.logging_in(self, self.username, self.password)
        response = test.api_get_call(self, '/api/get_course_assignments/' + str(course.pk) + '/', login_user)
        self.assertEquals(len(response.json()['assignments']), 2)
        self.assertIn('journal', response.json()['assignments'][0])

        login_rein = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/api/get_course_assignments/' + str(course.pk) + '/', login_rein)
        self.assertEquals(len(response.json()['assignments']), 2)

        test.unauthorized_api_get_call_test(self, '/api/get_course_assignments/' + str(course.pk) + '/')

    def test_get_course_roles(self):
        """Test the get delete assignment function."""
        teacher_user = 'Teacher'
        teacher_pass = 'pass'
        teacher = factory.make_user(teacher_user, teacher_pass)
        factory.make_role_ta("TA", self.course)
        factory.make_role_student("SD", self.course)
        factory.make_role_default_no_perms("HE", self.course)
        teacher_role = factory.make_role_teacher("TE", self.course)
        factory.make_participation(teacher, self.course, teacher_role)
        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_get_call(self, '/api/get_course_roles/1/', login)
        self.assertEquals(len(result.json()['roles']), 4)

        test.unauthorized_api_get_call_test(self, '/api/get_course_roles/1/')
