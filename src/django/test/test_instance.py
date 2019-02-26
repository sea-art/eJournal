import test.factory as factory
from test.utils import api

from django.test import TestCase


class InstanceAPITest(TestCase):

    def test_get(self):
        # Check if PK does not matter
        resp = api.get(self, 'instance', params={'pk': 0})
        assert resp['instance']['name'] == 'eJournal'
        resp = api.get(self, 'instance', params={'pk': 0})
        assert resp['instance']['name'] == 'eJournal'

    def test_update(self):
        api.update(self, 'instance', params={'pk': 0}, user=factory.Teacher(), status=403)

        admin = factory.Admin()
        resp = api.update(self, 'instance', params={'pk': 0, 'name': 'B1'}, user=admin)
        assert resp['instance']['name'] == 'B1'
