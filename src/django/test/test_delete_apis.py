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


class DeleteApiTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_delete_course(self):
        login = test.logging_in(self, self.username, self.password)

        bb = factory.make_course("Beeldbewerken", "BB")
        pav = factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        test.api_post_call(self, '/api/delete_course/', {'cID':  bb.pk}, login)

        self.assertEquals(Course.objects.filter(name="Beeldbewerken").count(), 0)
        self.assertEquals(Course.objects.filter(name="Portfolio Academische Vaardigheden").count(), 1)

    def delete_user_from_course(self):
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")
        pav = factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        rein = factory.make_user("Rein", "123")
        lars = factory.make_user("Lars", "123")

        factory.make_participation(rein, course)
        factory.make_participation(lars, course)

        test.api_post_call(self,
                           '/api/delete_user_from_course/',
                           {'cID': course.pk, 'uID': rein.user_role.pk},
                           login)

        participations = course.participation_set.all()
        participations = [serialize.participation_to_dict(participation)
                          for participation in participations]

        self.assertEquals(participations.count(), 1)
        self.assertEquals(participations[0]['name'], 'Lars')
