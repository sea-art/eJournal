from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import User
from VLE.models import Course


class RestTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

        c1 = Course(name="Portofolio Academische Vaardigheden",
                    abbreviation="PAV")
        c2 = Course(name="BeeldBewerken", abbreviation="BB")
        c3 = Course(name="Reflectie en Digitale Samenleving",
                    abbreviation="RDS")
        cs = [c1, c2, c3]
        for c in cs:
            c.save()
            c.participants.add(self.user)
            c.save()

    def test_get_user_courses(self):
        """
        Testing get_user_courses.
        """
        result = self.client.post(reverse('token_obtain_pair'),
                                  {'username': self.username,
                                   'password': self.password}, format='json')
        result = self.client.get(reverse('get_user_courses'), {},
                                 HTTP_AUTHORIZATION='Bearer {0}'.format(result.json()['access']))
        abbrev = result.json()['courses'][0]['abbreviation']
        eq = abbrev == 'RDS'
        eq |= abbrev == 'BB'
        eq |= abbrev == 'PAV'
        self.assertEquals(result.status_code, 200)
        self.assertEquals(eq, True)
