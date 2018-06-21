from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse
import json

from VLE.models import User
from VLE.models import Participation
from VLE.models import Role
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Entry

import VLE.factory as factory
import VLE.utils as utils
import json


def logging_in(obj, username, password, status=200):
    result = obj.client.post(reverse('token_obtain_pair'),
                             {'username': username, 'password': password},
                             format='json')
    obj.assertEquals(result.status_code, status)
    return result


def api_get_call(obj, url, login, status=200):
    result = obj.client.get(url, {},
                            HTTP_AUTHORIZATION='Bearer {0}'.format(login.data['access']))
    obj.assertEquals(result.status_code, status)
    return result


def api_post_call(obj, url, params, login, status=200):
    result = obj.client.post(url, json.dumps(params), content_type='application/json',
                             HTTP_AUTHORIZATION='Bearer {0}'.format(login.data['access']))
    obj.assertEquals(result.status_code, status)
    return result


class RestTests(TestCase):
    """
    Test django rest api calls
    """
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)
        self.student = factory.make_user('Student', 'pass')

        u1 = factory.make_user("Zi-Long", "pass")
        u2 = factory.make_user("Rick", "pass")
        u3 = factory.make_user("Lars", "pass")
        u4 = factory.make_user("Jeroen", "pass")

        c1 = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        c2 = factory.make_course("BeeldBewerken", "BB")
        c3 = factory.make_course("Reflectie en Digitale Samenleving", "RDS")

        self.user_role = factory.make_user("test123", "test")
        role = factory.make_role(name='TA', can_view_assignment=True)
        studentRole = factory.make_role(name='SD')

        factory.make_participation(self.user_role, c1, role)

        cs = [c1, c2, c3]
        for c in cs:
            c.save()
            p = Participation()
            p.user = self.user
            p.course = c
            p.role = role
            p.save()
            c.participation_set.add(p)
            c.save()

            p = Participation()
            p.user = self.student
            p.course = c
            p.role = studentRole
            p.save()
            c.participation_set.add(p)
            c.save()

        t = factory.make_entry_template('template_test')
        f = factory.make_format([t], 5)
        a1 = factory.make_assignment("Colloq", "In de opdracht...1", u1, format=f)
        a2 = factory.make_assignment("Logboek", "In de opdracht...2", u1)
        a1.courses.add(c1)
        a1.courses.add(c2)
        a2.courses.add(c1)

        j2 = factory.make_journal(a1, u3)
        j3 = factory.make_journal(a1, u4)

        j = factory.make_journal(a1, self.student)
        jj = factory.make_journal(a1, u2)
        e1 = factory.make_entry(t)
        e2 = factory.make_entry(t)
        e3 = factory.make_entry(t)
        e4 = factory.make_entry(t)
        n1 = factory.make_node(j, e1)
        n2 = factory.make_node(j, e2)
        n3 = factory.make_node(j, e3)
        n4 = factory.make_node(jj, e4)

    def test_login(self):
        """
        Tests if the login is successful.
        """
        result = logging_in(self, self.username, self.password)
        self.assertEquals(result.status_code, 200)

    def test_not_logged_in(self):
        """
        Tests error for api request call for non-authenticated user.
        """
        result = self.client.get(reverse('get_user_courses'), {}, format='json')
        self.assertEquals(result.status_code, 401)

    def test_get_user_courses(self):
        """
        Tests get_user_courses
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
        Tests get_course_assignments
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

    def test_student_get_course_assignments(self):
        """
        Tests get_course_assignments for student.
        """
        login = logging_in(self, 'Student', 'pass')
        result = api_get_call(self, '/api/get_course_assignments/1/', login)
        assignments = result.json()['assignments']

        self.assertEquals(len(assignments), 2)
        self.assertEquals(assignments[0]['name'], 'Colloq')

        result = api_get_call(self, '/api/get_course_assignments/2/', login)
        assignments = result.json()['assignments']

        self.assertEquals(len(assignments), 1)

    def test_get_assignment_journals(self):
        """
        Tests get_assignment_journals
        """
        login = logging_in(self, self.username, self.password)
        result = api_get_call(self, '/api/get_assignment_journals/1/', login)
        journals = result.json()['journals']
        self.assertEquals(len(journals), 4)
        self.assertEquals(journals[0]['student']['name'], 'Student')
        self.assertEquals(journals[1]['student']['name'], 'Rick')
        self.assertEquals(journals[2]['student']['name'], 'Lars')
        self.assertEquals(journals[3]['student']['name'], 'Jeroen')

    def test_journal_stats(self):
        """
        Tests the journal stats functions in the serializer.
        """
        journal = Journal.objects.get(user=self.student)
        entries = utils.get_journal_entries(journal)
        for i in range(len(entries)):
            if i > 0:
                entries[i].grade = 1
                entries[i].published = True
                entries[i].save()
        self.assertEquals(utils.get_acquired_grade(entries, journal), 2)
        self.assertEquals(utils.get_max_points(journal), 5)
        self.assertEquals(utils.get_submitted_count(entries), 3)
        self.assertEquals(utils.get_graded_count(entries), 2)

    def test_update_user_role_course(self):
        """
        Tests user role update in a course.
        """
        user_role = Participation.objects.get(user=self.user_role, course=1).role.name
        self.assertEquals(user_role, 'TA')

        login = logging_in(self, self.username, self.password)
        result = api_post_call(
            self,
            '/api/update_user_role_course/',
            {'cID': 1, 'uID': self.user_role.pk, 'role': 'SD'},
            login
            )
        user_role = Participation.objects.get(user=self.user_role, course=1).role.name
        self.assertEquals(user_role, 'SD')

    def test_grade_publish(self):
        """
        Tests the grade publish api functions.
        """
        login = logging_in(self, self.username, self.password)
        result = api_post_call(self, '/api/update_grade_entry/1/', {'grade': 1, 'published': 0}, login)
        self.assertEquals(Entry.objects.get(pk=1).grade, int(result.json()['new_grade']))

        result = api_post_call(self, '/api/update_grade_entry/1/', {'grade': 2, 'published': 1}, login)
        self.assertEquals(Entry.objects.get(pk=1).grade, int(result.json()['new_grade']))
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))

        result = api_post_call(self, '/api/update_publish_grade_entry/1/', {'published': 0}, login)
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))

        api_post_call(self, '/api/update_grade_entry/2/', {'grade': 1, 'published': 0}, login)
        api_post_call(self, '/api/update_grade_entry/4/', {'grade': 1, 'published': 0}, login)
        result = api_post_call(self, '/api/update_publish_grades_assignment/1/', {'published': 1}, login)
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))
        self.assertEquals(Entry.objects.get(pk=2).published, int(result.json()['new_published']))
        self.assertEquals(Entry.objects.get(pk=3).published, 0)
        self.assertEquals(Entry.objects.get(pk=4).published, int(result.json()['new_published']))

        result = api_post_call(self, '/api/update_publish_grades_journal/3/', {'published': 0}, login)
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))
        self.assertEquals(Entry.objects.get(pk=2).published, int(result.json()['new_published']))
        self.assertEquals(Entry.objects.get(pk=3).published, 0)
