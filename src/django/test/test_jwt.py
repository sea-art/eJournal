from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import User


class JWTTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = User(username=self.username)
        self.user.set_password(self.password)
        self.user.save()

    def test_get_auth(self):
        """
        Testing simple authentication with JWT keys.
        """

        result = self.client.post(reverse('token_obtain_pair'),
                                  {'username': self.username,
                                   'password': self.password}, format='json')

        self.assertEquals(result.status_code, 200)
        self.assertTrue(result.json()['access'])
        self.assertTrue(result.json()['refresh'])

    def test_anonymous(self):
        """
        Testing simple anonymous access.
        """

        result = self.client.get(reverse('get_user_courses'), {}, format='json')

        self.assertEquals(result.status_code, 401)

    def test_user(self):
        """
        Testing authenticated access.
        """
        result = self.client.post(reverse('token_obtain_pair'),
                                  {'username': self.username,
                                   'password': self.password}, format='json')

        result = self.client.get(reverse('get_user_courses'), {},
                                 HTTP_AUTHORIZATION='Bearer {0}'.format(result.json()['access']))
        
        self.assertEquals(result.status_code, 200)
        self.assertEquals(result.json()['result'], 'success')
        self.assertEquals(result.json()['courses'], [])
