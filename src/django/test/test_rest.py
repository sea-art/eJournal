from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import *


class RestTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = User(username=self.username)
        self.user.save()
        self.user.set_password(self.password)
        self.user.save()

        c1 = Course(name="Portofolio Academische Vaardigheden",
                    abbreviation="PAV")
        c2 = Course(name="BeeldBewerken", abbreviation="BB")
        c3 = Course(name="Reflectie en Digitale Samenleving",
                    abbreviation="RDS")
        role = Role(name='TA')
        role.save()

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

    def test_get_user_courses(self):
        """
        Testing get_user_courses.
        """
        result = self.client.get(reverse('get_user_courses'), {}, format='json')
        self.assertEquals(result.status_code, 401)

        result = self.client.post(reverse('token_obtain_pair'),
                                  {'username': self.username,
                                   'password': self.password}, format='json')
        self.assertEquals(result.status_code, 200)

        result = self.client.get(reverse('get_user_courses'), {},
                                 HTTP_AUTHORIZATION='Bearer {0}'.format(result.data['access']))
        self.assertEquals(result.status_code, 200)
        courses = result.json()['courses']
        self.assertEquals(len(courses), 3)
        self.assertEquals(courses[0]['abbr'], 'PAV')
        self.assertEquals(courses[1]['abbr'], 'BB')
        self.assertEquals(courses[2]['abbr'], 'RDS')
