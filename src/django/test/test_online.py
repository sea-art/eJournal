from django.test import Client
from django.test import TestCase


class IsOnline(TestCase):
    def setUp(self):
        self.c = Client()

    def test_online(self):
        response = self.c.get('/admin', follow=True)
        self.assertEquals(response.status_code, 200)
