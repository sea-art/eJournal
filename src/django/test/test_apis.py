from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse

from VLE.models import User
from VLE.models import Participation
from VLE.models import Role
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Field

import VLE.factory as factory
import VLE.utils as utils

import test.test_rest as test
import json as json


class ApiTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_get_course_users(self):
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        rein = factory.make_user("Rein", "123")
        lars = factory.make_user("Lars", "123")
        zi = factory.make_user("Zi", "123")

        TA = factory.make_role("TA")
        SD = factory.make_role("SD")
        factory.make_participation(rein, course, TA)
        factory.make_participation(lars, course, SD)

        response = test.api_get_call(self, '/api/get_course_users/' + str(course.pk) + '/', login)

        self.assertEquals(len(response.json()['users']), 2)

    def test_get_template(self):
        login = test.logging_in(self, self.username, self.password)

        template = factory.make_entry_template("template")
        field = factory.make_field(template, "Some Field", 0)
        field2 = factory.make_field(template, "Some other Field", 1)

        response = test.api_get_call(self, '/api/get_template/' + str(template.pk) + '/', login)

        self.assertEquals(response.json()['template']['tID'], template.pk)
        self.assertEquals(response.json()['template']['name'], "template")
        self.assertEquals(len(response.json()['template']['fields']), 2)

    def test_create_template(self):
        login = test.logging_in(self, self.username, self.password)

        data = {
            "name": "template",
            "fields": [
                {"type": Field.TEXT, "title": "Some Field", "location": 0},
                {"type": Field.TEXT, "title": "Some Other Field", "location": 1},
            ]
        }
        response = test.api_post_call(self, '/api/update_template/', data, login)

        self.assertEquals(response.json()['template']['name'], "template")
        self.assertEquals(len(response.json()['template']['fields']), 2)

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

        response = test.api_post_call(self, '/api/create_entry/', some_dict, login)
