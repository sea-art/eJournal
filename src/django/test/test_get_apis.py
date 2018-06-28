"""
test_get_apis.py.

Test the get apis.
"""
from django.test import TestCase

import VLE.factory as factory

import test.test_utils as test
from VLE.models import Role


class GetApiTests(TestCase):
    """Get Api tests.

    Test the get apis.
    """

    def setUp(self):
        """Set up the test file."""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')
        self.rein_user, self.rein_pass, self.rein = test.set_up_user_and_auth("Rein", "123")
        self.no_perm_user, self.no_perm_pass, self.no_permission_user = test.set_up_user_and_auth("no_perm", "123")
        self.course = factory.make_course("Beeldbewerken", "BB")
        self.lars = factory.make_user("Lars", "123")
        self.not_found_pk = 9999

    def test_get_own_user_data(self):
        """Test the get own user data function."""
        login = test.logging_in(self, self.username, self.password)
        response = test.api_get_call(self, '/get_own_user_data/', login)

        self.assertEquals(response.json()['user']['name'], self.username)

        # permissions and authorization check for the api call.
        test.test_unauthorized_api_get_call(self, '/get_own_user_data/')

    def test_get_course_data(self):
        """Test get coursedata function."""
        test.set_up_participation(self.user, self.course, 'Teacher')
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/get_course_data/' + str(self.course.pk) + '/', login)

        self.assertEquals(response.json()['course']['name'], 'Beeldbewerken')
        self.assertEquals(response.json()['course']['abbr'], 'BB')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_course_data/' + str(self.course.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_course_data/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_course_data/' + str(self.course.pk) + '/')

    def test_get_course_users(self):
        """Test the get course users function."""
        teacher_user, teacher_pass, teacher = test.set_up_user_and_auth('teacher', 'pass')
        test.set_up_participation(teacher, self.course, 'Teacher')
        test.set_up_participation(self.lars, self.course, 'Student')
        test.set_up_participation(self.rein, self.course, 'TA')

        login = test.logging_in(self, teacher_user, teacher_pass)

        response = test.api_get_call(self, '/get_course_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 3)

        response = test.api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 2)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_course_users/' + str(self.course.pk) + '/', login, status=403)
        test.api_get_call(self,  '/get_course_users/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self,  '/get_course_users/' + str(self.course.pk) + '/')
        test.test_unauthorized_api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/')

        test.set_up_participation(self.no_permission_user, self.course, 'Student')
        test.api_get_call(self, '/get_course_users/' + str(self.course.pk) + '/', login, status=403)

    def test_get_unenrolled_users(self):
        """Test the get get_unenrolledusers."""
        teacher_user, teacher_pass, teacher = test.set_up_user_and_auth('teacher', 'pass')
        test.set_up_participation(teacher, self.course, 'Teacher')
        test.set_up_participation(self.lars, self.course, 'Student')
        test.set_up_participation(self.rein, self.course, 'TA')

        login = test.logging_in(self, teacher_user, teacher_pass)

        response = test.api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 2)
        self.assertEquals(response.json()['users'][0]['name'], self.username)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_unenrolled_users/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/')

        test.set_up_participation(self.no_permission_user, self.course, 'Student')
        test.api_get_call(self, '/get_unenrolled_users/' + str(self.course.pk) + '/', login, status=403)

    def test_get_user_courses(self):
        """Test the get user courses function."""
        for course in test.set_up_courses('course', 4):
            student_role = Role.objects.get(name='Student', course=course)
            factory.make_participation(self.user, course, student_role)

        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/get_user_courses/', login)
        self.assertEquals(len(response.json()['courses']), 4)

        # permissions and authorization check for the api call.
        test.test_unauthorized_api_get_call(self, '/get_user_courses/')

    def test_get_linkable_courses(self):
        """Test the get linkable courses function."""
        self.user.is_teacher = True
        self.user.save()

        test.set_up_courses('course', 3, author=self.user)
        test.set_up_courses('course', 4, author=self.user, lti_id=True)

        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/get_linkable_courses/', login)
        self.assertEquals(len(response.json()['courses']), 3)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_linkable_courses/', login, status=403)
        test.test_unauthorized_api_get_call(self, '/get_linkable_courses/')

    def test_get_course_assignments(self):
        """Test the get course assignment function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        assigns = test.set_up_assignments('assign', 'desc', 2, course=course)
        test.set_up_participation(self.user, course, 'Student')
        factory.make_journal(assigns[0], self.user)
        factory.make_journal(assigns[1], self.user)

        login_user = test.logging_in(self, self.username, self.password)
        response = test.api_get_call(self, '/get_course_assignments/' + str(course.pk) + '/', login_user)
        self.assertEquals(len(response.json()['assignments']), 2)
        self.assertIn('journal', response.json()['assignments'][0])

        login_rein = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/get_course_assignments/' + str(course.pk) + '/', login_rein)
        self.assertEquals(len(response.json()['assignments']), 2)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_course_assignments/' + str(course.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_course_assignments/' + str(self.not_found_pk) + '/', login_user, status=404)
        test.test_unauthorized_api_get_call(self, '/get_course_assignments/' + str(course.pk) + '/')

    def test_get_assignment_data(self):
        """Test the get assignment data function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format1 = factory.make_format([template], 10)
        format2 = factory.make_format([template], 10)
        assignment1 = factory.make_assignment('Colloq', 'description1', format=format1, courses=[course])
        assignment2 = factory.make_assignment('Portfolio', 'description2', format=format2, courses=[course])

        test.set_up_participation(self.user, course, 'Student')

        login_user = test.logging_in(self, self.username, self.password)
        resp = test.api_get_call(self, '/get_assignment_data/' + str(course.pk) + '/' + str(assignment1.pk) + '/',
                                 login_user)
        self.assertEquals(resp.json()['assignment']['name'], 'Colloq')
        self.assertIn('journal', resp.json()['assignment'])

        login_rein = test.logging_in(self, self.rein_user, self.rein_pass)
        resp = test.api_get_call(self, '/get_assignment_data/' + str(course.pk) + '/' + str(assignment2.pk) + '/',
                                 login_rein)
        self.assertEquals(resp.json()['assignment']['name'], 'Portfolio')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_assignment_data/' + str(course.pk) + '/' + str(assignment1.pk) + '/',
                          login, status=403)
        test.api_get_call(self, '/get_assignment_data/' + str(self.not_found_pk) + '/' + str(assignment2.pk) + '/',
                          login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_assignment_data/1/' + str(assignment1.pk) + '/')

    def test_assignment_journals(self):
        """Test the get assignment journals function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        assignment = factory.make_assignment('Colloq', 'description1', format=format, courses=[course])
        students = test.set_up_users('student', 2)
        for student in students:
            test.set_up_participation(student, course, 'Student')
            test.set_up_journal(assignment, template, student, 4)

        login = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/get_assignment_journals/' + str(assignment.pk) + '/', login)
        result = response.json()
        self.assertEquals(len(result['journals']), 2)
        self.assertEquals(result['stats']['needsMarking'], 8)
        self.assertEquals(result['stats']['avgPoints'], 0)
        self.assertEquals(result['stats']['medianPoints'], 0)
        self.assertEquals(result['stats']['avgEntries'], 4)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_assignment_journals/' + str(assignment.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_assignment_journals/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_assignment_journals/' + str(self.not_found_pk) + '/')

    def test_get_nodes(self):
        """Test the get nodes function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        assignment = factory.make_assignment('Colloq', 'description1', format=format, courses=[course])
        student_user, student_pass, student = test.set_up_user_and_auth('student', 'pass')
        test.set_up_participation(student, course, 'Student')
        journal = test.set_up_journal(assignment, template, student, 4)

        login = test.logging_in(self, student_user, student_pass)
        response = test.api_get_call(self, '/get_nodes/' + str(journal.pk) + '/', login)
        result = response.json()
        self.assertEquals(len(result['nodes']), 4)

        login = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/get_nodes/' + str(journal.pk) + '/', login)
        result = response.json()
        self.assertEquals(len(result['nodes']), 4)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_nodes/' + str(journal.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_nodes/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_nodes/' + str(journal.pk) + '/')

    def test_get_format(self):
        """Test get format."""
        course1 = factory.make_course('Portfolio2016', 'PAV', author=self.rein)
        course2 = factory.make_course('Portfolio2017', 'PAV', author=self.rein)
        course3 = factory.make_course('Portfolio2018', 'PAV')
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        assignment = factory.make_assignment('Colloq', 'description1', format=format,
                                             courses=[course1, course2, course3])
        login = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/get_format/' + str(assignment.pk) + '/', login)
        self.assertEquals(response.json()['format']['templates'][0]['name'], 'template')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_format/' + str(assignment.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_format/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_format/' + str(assignment.pk) + '/')

    def test_get_course_roles(self):
        """Test the get delete assignment function."""
        teacher_user = 'Teacher'
        teacher_pass = 'pass'
        teacher = factory.make_user(teacher_user, teacher_pass)
        factory.make_role_student("SD", self.course)
        factory.make_role_default_no_perms("HE", self.course)
        teacher_role = factory.make_role_teacher("TE", self.course)
        factory.make_participation(teacher, self.course, teacher_role)
        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_get_call(self, '/get_course_roles/1/', login)
        self.assertEquals(len(result.json()['roles']), 6)

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.test_unauthorized_api_get_call(self, '/get_course_roles/1/')
        test.api_get_call(self, '/get_course_roles/1/', login, status=403)
        test.api_get_call(self, '/get_course_roles/' + str(self.not_found_pk) + '/', login, status=404)

        test.set_up_participation(self.no_permission_user, self.course, 'Student')
        test.api_get_call(self, '/get_course_roles/1/', login, status=403)

    def test_get_user_teacher_courses(self):
        """Test get user teacher course function."""
        factory.make_course('Portfolio2016', 'PAV', author=self.rein)
        factory.make_course('Portfolio2017', 'PAV', author=self.rein)
        factory.make_course('Portfolio2018', 'PAV')

        login = test.logging_in(self, self.rein_user, self.rein_pass)
        response = test.api_get_call(self, '/get_user_teacher_courses/', login)
        self.assertEquals(len(response.json()['courses']), 2)

        # permissions and authorization check for the api call.
        test.test_unauthorized_api_get_call(self, '/get_user_teacher_courses/')

    def test_get_names(self):
        """Test get names function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        assignment = factory.make_assignment('Colloq', 'description1', format=format, courses=[course])
        student_user, student_pass, student = test.set_up_user_and_auth('student', 'pass')
        test.set_up_participation(student, course, 'Student')
        journal = test.set_up_journal(assignment, template, student, 4)

        get_names_dict = {'cID': course.pk, 'aID': assignment.pk, 'jID': journal.pk}
        get_not_found_dict = {'cID': self.not_found_pk, 'aID': assignment.pk, 'jID': journal.pk}

        login = test.logging_in(self, student_user, student_pass)

        result = test.api_post_call(self, '/get_names/', get_names_dict, login).json()
        self.assertEquals(result['course'], 'Portfolio')
        self.assertEquals(result['journal'], 'student')
        self.assertEquals(result['assignment'], 'Colloq')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.test_unauthorized_api_post_call(self, '/get_names/', get_names_dict)
        test.api_post_call(self, '/get_names/', get_names_dict, login, status=403)
        test.api_post_call(self, '/get_names/', get_not_found_dict, login, status=404)

    def test_get_entrycomments(self):
        """Test get entrycomments function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        assignment = factory.make_assignment('Colloq', 'description1', format=format, courses=[course])
        student_user, student_pass, student = test.set_up_user_and_auth('student', 'pass')
        test.set_up_participation(student, course, 'Student')
        journal = factory.make_journal(assignment, student)
        entry = factory.make_entry(template)
        factory.make_node(journal, entry)
        factory.make_entrycomment(entry, self.rein, 'Excellent!')

        login = test.logging_in(self, student_user, student_pass)

        result = test.api_get_call(self, '/get_entrycomments/' + str(entry.pk) + '/', login).json()
        self.assertEquals(result['entrycomments'][0]['text'], 'Excellent!')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_entrycomments/' + str(entry.pk) + '/', login, status=403)
        test.api_get_call(self, '/get_entrycomments/' + str(self.not_found_pk) + '/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_entrycomments/' + str(entry.pk) + '/')

    def test_get_assignment_by_lti_id(self):
        """Test get assignment by lti id function."""
        course = factory.make_course('Portfolio', 'PAV', author=self.rein)
        template = factory.make_entry_template('template')
        format = factory.make_format([template], 10)
        factory.make_assignment('Colloq', 'description1', format=format, courses=[course], lti_id='12xy')

        login = test.logging_in(self, self.rein_user, self.rein_pass)
        result = test.api_get_call(self, '/get_assignment_by_lti_id/12xy/', login).json()
        self.assertEquals(result['assignment']['name'], 'Colloq')

        # permissions and authorization check for the api call.
        login = test.logging_in(self, self.no_perm_user, self.no_perm_pass)
        test.api_get_call(self, '/get_assignment_by_lti_id/12xy/', login, status=403)
        test.api_get_call(self, '/get_assignment_by_lti_id/random/', login, status=404)
        test.test_unauthorized_api_get_call(self, '/get_assignment_by_lti_id/12xy/')
