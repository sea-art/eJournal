from django.test import TestCase

from VLE.models import Course

import VLE.factory as factory

import VLE.serializers as serialize

import test.test_rest as test


class DeleteApiTests(TestCase):
    def setUp(self):
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_delete_course(self):
        login = test.logging_in(self, self.username, self.password)

        bb = factory.make_course("Beeldbewerken", "BB")
        factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        test.api_post_call(self, '/api/delete_course/', {'cID':  bb.pk}, login)

        self.assertEquals(Course.objects.filter(name="Beeldbewerken").count(), 0)
        self.assertEquals(Course.objects.filter(name="Portfolio Academische Vaardigheden").count(), 1)

    def delete_user_from_course(self):
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

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
