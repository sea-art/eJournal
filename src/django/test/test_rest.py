from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal

import VLE.util as util


def logging_in(obj, username, password):
    result = obj.client.post(reverse('token_obtain_pair'),
                             {'username': username, 'password': password}, format='json')
    obj.assertEquals(result.status_code, 200)
    return result


def api_get_call(obj, url, login):
    result = obj.client.get(url, {},
                            HTTP_AUTHORIZATION='Bearer {0}'.format(login.data['access']))
    obj.assertEquals(result.status_code, 200)
    return result


class RestTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = util.make_user(self.username, self.password)

        u1 = util.make_user("Zi-Long", "pass")
        u2 = util.make_user("Rick", "pass")
        u3 = util.make_user("Lars", "pass")
        u4 = util.make_user("Jeroen", "pass")

        c1 = util.make_course("Portofolio Academische Vaardigheden", "PAV")
        c2 = util.make_course("BeeldBewerken", "BB")
        c3 = util.make_course("Reflectie en Digitale Samenleving", "RDS")

        cs = [c1, c2, c3]
        for c in cs:
            c.participants.add(self.user)

        a1 = util.make_assignment("Colloq", "In de opdracht...1", u1)
        a2 = util.make_assignment("Logboek", "In de opdracht...2", u1)
        a1.courses.add(c1)
        a1.courses.add(c2)
        a2.courses.add(c1)

        j1 = util.make_journal(a1, u2)
        j2 = util.make_journal(a1, u3)
        j3 = util.make_journal(a1, u4)

    def test_login(self):
        result = logging_in(self, self.username, self.password)

    def test_not_logged_in(self):
        result = self.client.get(reverse('get_user_courses'), {}, format='json')
        self.assertEquals(result.status_code, 401)

    def test_get_user_courses(self):
        """
        Testing get_user_courses.
        """
        login = logging_in(self, self.username, self.password)

        result = api_get_call(self, reverse('get_user_courses'), login)
        courses = result.json()['courses']
        self.assertEquals(len(courses), 3)
        self.assertEquals(courses[0]['abbr'], 'PAV')
        self.assertEquals(courses[1]['abbr'], 'BB')
        self.assertEquals(courses[2]['abbr'], 'RDS')

    def test_get_course_assignments(self):
        """
        Testing get_course_assignments
        """
        login = logging_in(self, self.username, self.password)
        result = api_get_call(self, '/api/get_course_assignments/1/', login)
        assignments = result.json()['assignments']

        self.assertEquals(len(assignments), 2)
        self.assertEquals(assignments[0]['name'], 'Colloq')
        self.assertEquals(assignments[1]['name'], 'Logboek')

        result = api_get_call(self, '/api/get_course_assignments/2/', login)
        assignments = result.json()['assignments']

        self.assertEquals(assignments[0]['name'], 'Colloq')
        self.assertEquals(assignments[0]['description'], 'In de opdracht...1')

    def test_get_assignment_journals(self):
        login = logging_in(self, self.username, self.password)
        result = api_get_call(self, '/api/get_assignment_journals/1/', login)
        journals = result.json()['journals']
        self.assertEquals(len(journals), 3)
        self.assertEquals(journals[0]['student'], 'Rick')
        self.assertEquals(journals[1]['student'], 'Lars')
