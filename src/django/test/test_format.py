import test.factory as factory
from test.utils import api

from django.test import TestCase

import VLE.serializers as serialize
from VLE.models import Journal


class FormatAPITest(TestCase):
    def setUp(self):
        self.teacher = factory.Teacher()
        self.admin = factory.Admin()
        self.course = factory.Course(author=self.teacher)
        self.assignment = factory.Assignment(courses=[self.course])
        self.format = factory.Format(assignment=self.assignment)
        self.template = factory.Template(format=self.format)
        self.update_dict = {
            'assignment_details': {
                'name': 'Colloq',
                'description': 'description1',
                'is_published': True
            },
            'templates': serialize.TemplateSerializer(self.format.template_set.filter(archived=False), many=True).data,
            'removed_presets': [],
            'removed_templates': [],
            'presets': []
        }

    def test_update(self):
        # TODO: Improve template testing
        api.update(
            self, 'formats', params={
                'pk': self.assignment.pk, 'assignment_details': None,
                'templates': [], 'presets': [], 'removed_presets': [],
                'removed_templates': []
            }, user=factory.Student(), status=403)
        api.update(
            self, 'formats', params={
                'pk': self.assignment.pk, 'assignment_details': None,
                'templates': [], 'presets': [], 'removed_presets': [],
                'removed_templates': []
            }, user=self.teacher)
        api.update(
            self, 'formats', params={
                'pk': self.assignment.pk, 'assignment_details': None,
                'templates': [], 'presets': [], 'removed_presets': [],
                'removed_templates': []
            }, user=factory.Admin())

        # Try to publish the assignment
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=factory.Student(), status=403)
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=self.teacher)
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=factory.Admin())

        # Check cannot unpublish if there are journals
        self.update_dict['assignment_details']['is_published'] = False
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=self.teacher, status=400)
        Journal.objects.filter(assignment=self.assignment).delete()
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=self.teacher, status=200)
        self.update_dict['assignment_details']['is_published'] = True
        api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                   user=self.teacher, status=200)

        # Test script sanitation
        self.update_dict['assignment_details']['description'] = '<script>alert("asdf")</script>Rest'
        resp = api.update(self, 'formats', params={'pk': self.assignment.pk, **self.update_dict},
                          user=self.teacher)
        assert resp['assignment_details']['description'] == 'Rest'
