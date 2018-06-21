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

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.json()['users']), 2)
