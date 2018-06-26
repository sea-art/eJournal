from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import User
from VLE.models import Participation
from VLE.models import Role
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal

import VLE.factory as factory
import VLE.utils as utils

import test.test_rest as test
import json as json


class CreateApiTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_create_entry(self):
        login = test.logging_in(self, self.username, self.password)

        assignment = factory.make_assignment("Assignment", "Your favorite assignment")
        journal = factory.make_journal(assignment, self.user)
        template = factory.make_entry_template("some_template")
        field = factory.make_field(template, 'Some field', 0)

        some_dict = {
            'jID': journal.id,
            'tID': template.id,
            'content': [{
                'tag': field.pk,
                'data': "This is some data"
                }]
            }

        response = test.api_post_call(self, '/api/create_entry/', some_dict, login, 201)
