from django.test import TestCase
from django.urls import reverse

import VLE.factory as factory
import test.test_rest as test


class GetApiTests(TestCase):
    def setUp(self):
        """Setup"""
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_get_own_user_data(self):
        """Test get_own_user_data"""
        login = test.logging_in(self, self.username, self.password)

        response = test.api_get_call(self, '/api/get_own_user_data/', login)

        self.assertEquals(response.json()['user']['name'], self.username)

    def test_course_data(self):
        """Test get_course_data"""
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        response = test.api_get_call(self, '/api/get_course_data/' + str(course.pk) + '/', login)

        self.assertEquals(response.json()['course']['name'], 'Beeldbewerken')
        self.assertEquals(response.json()['course']['abbr'], 'BB')

    def test_get_user_courses(self):
        """Test get_user_courses."""
        login = test.logging_in(self, self.username, self.password)

        course1 = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        course2 = factory.make_course("BeeldBewerken", "BB")
        course3 = factory.make_course("Reflectie en Digitale Samenleving", "RDS")

        cs = [course1, course2, course3]
        for c in cs:
            factory.make_participation(self.user, c)

        result = test.api_get_call(self, reverse('get_user_courses'), login)

        courses = result.json()['courses']

        self.assertEquals(len(courses), 3)
        self.assertEquals(courses[0]['abbr'], 'PAV')
        self.assertEquals(courses[1]['abbr'], 'BB')
        self.assertEquals(courses[2]['abbr'], 'RDS')

    def test_get_course_users(self):
        """Test get_course_users"""
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

    def test_get_course_assignments(self):
        """Test get_course_assignments."""
        login = test.logging_in(self, self.username, self.password)

        course1 = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        course2 = factory.make_course("BeeldBewerken", "BB")

        role = factory.make_role(name='TA', can_grade_journal=True, can_view_assignment_participants=True)

        factory.make_participation(self.user, course1, role)
        factory.make_participation(self.user, course2, role)

        assign1 = factory.make_assignment("Colloq", "In de opdracht...1", self.user)
        assign2 = factory.make_assignment("Logboek", "In de opdracht...2", self.user)
        assign1.courses.add(course1)
        assign1.courses.add(course2)
        assign2.courses.add(course1)

        result = test.api_get_call(self, '/api/get_course_assignments/1/', login)

        assignments = result.json()['assignments']
        self.assertEquals(len(assignments), 2)
        self.assertEquals(assignments[0]['name'], 'Colloq')
        self.assertEquals(assignments[1]['name'], 'Logboek')

        result = test.api_get_call(self, '/api/get_course_assignments/2/', login)
        assignments = result.json()['assignments']

        self.assertEquals(assignments[0]['name'], 'Colloq')
        self.assertEquals(assignments[0]['description'], 'In de opdracht...1')

    def test_student_get_course_assignments(self):
        """Test get_course_assignments for student."""
        login = test.logging_in(self, self.username, self.password)

        course1 = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        course2 = factory.make_course("BeeldBewerken", "BB")

        role = factory.make_role(name='TA', can_grade_journal=True, can_view_assignment_participants=True)

        factory.make_participation(self.user, course1, role)
        factory.make_participation(self.user, course2, role)

        assign1 = factory.make_assignment("Colloq", "In de opdracht...1", self.user)
        assign2 = factory.make_assignment("Logboek", "In de opdracht...2", self.user)
        assign1.courses.add(course1)
        assign1.courses.add(course2)
        assign2.courses.add(course1)

        result = test.api_get_call(self, '/api/get_course_assignments/1/', login)
        assignments = result.json()['assignments']

        self.assertEquals(len(assignments), 2)
        self.assertEquals(assignments[0]['name'], 'Colloq')

        result = test.api_get_call(self, '/api/get_course_assignments/2/', login)
        assignments = result.json()['assignments']

        self.assertEquals(len(assignments), 1)

    def test_get_assignment_journals(self):
        """Test get_assignment_journals."""
        login = test.logging_in(self, self.username, self.password)

        user2 = factory.make_user("Rick", "pass")
        user3 = factory.make_user("Lars", "pass")
        user4 = factory.make_user("Jeroen", "pass")

        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        assign = factory.make_assignment("Colloq", "In de opdracht...1", self.user)
        assign.courses.add(course)

        role = factory.make_role(name='TA', can_grade_journal=True, can_view_assignment_participants=True)

        factory.make_participation(self.user, course, role)
        factory.make_participation(user2, course)
        factory.make_participation(user3, course)
        factory.make_participation(user4, course)

        factory.make_journal(assign, self.user)
        factory.make_journal(assign, user2)
        factory.make_journal(assign, user3)
        factory.make_journal(assign, user4)

        result = test.api_get_call(self, '/api/get_assignment_journals/1/', login)
        journals = result.json()['journals']

        self.assertEquals(len(journals), 4)
        self.assertEquals(journals[0]['student']['name'], 'test')
        self.assertEquals(journals[1]['student']['name'], 'Rick')
        self.assertEquals(journals[2]['student']['name'], 'Lars')
        self.assertEquals(journals[3]['student']['name'], 'Jeroen')

    def test_get_unenrolled_users(self):
        """Test get_unenrolled_users"""
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
