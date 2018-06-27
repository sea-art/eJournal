from django.test import TestCase

from VLE.models import Course, Assignment, Role

import VLE.factory as factory
import VLE.serializers as serialize
import test.test_utils as test


class DeleteApiTests(TestCase):
    def setUp(self):
        """Setup"""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')
        self.course = factory.make_course("Beeldbewerken", "BB")

    def test_delete_course(self):
        """Test delete_course"""
        login = test.logging_in(self, self.username, self.password)

        bb = factory.make_course("Beeldbewerken", "BB")
        factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        test.api_post_call(self, '/delete_course/', {'cID':  bb.pk}, login)

        self.assertEquals(Course.objects.filter(name="Beeldbewerken").count(), 1)
        self.assertEquals(Course.objects.filter(name="Portfolio Academische Vaardigheden").count(), 1)

    def delete_user_from_course(self):
        """Test delete_user_from_course"""
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Beeldbewerken", "BB")

        rein = factory.make_user("Rein", "123")
        lars = factory.make_user("Lars", "123")

        factory.make_participation(rein, course)
        factory.make_participation(lars, course)

        test.api_post_call(self,
                           '/delete_user_from_course/',
                           {'cID': course.pk, 'uID': rein.user_role.pk},
                           login)

        participations = course.participation_set.all()
        participations = [serialize.participation_to_dict(participation)
                          for participation in participations]

        self.assertEquals(participations.count(), 1)
        self.assertEquals(participations[0]['name'], 'Lars')

    def test_delete_assignment(self):
        """Test delete_assignment."""
        login = test.logging_in(self, self.username, self.password)

        user = factory.make_user("Zi-Long", "pass")

        course1 = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        course2 = factory.make_course("BeeldBewerken", "BB")

        assign1 = factory.make_assignment("Colloq", "In de opdracht...1", user)
        assign2 = factory.make_assignment("Logboek", "In de opdracht...2", user)

        assign1.courses.add(course1)
        assign1.courses.add(course2)
        assign2.courses.add(course1)

        test.api_post_call(self, '/delete_assignment/', {'cID': 1, 'aID': 1}, login)
        assignment = Assignment.objects.get(pk=1)
        self.assertEquals(assignment.courses.count(), 2)

        test.api_post_call(self, '/delete_assignment/', {'cID': 2, 'aID': 1}, login)
        self.assertEquals(Assignment.objects.filter(pk=1).count(), 1)

    def test_delete_course_role(self):
        """Test delete course roles"""
        teacher_user = 'Teacher'
        teacher_pass = 'pass'
        teacher = factory.make_user(teacher_user, teacher_pass)
        teacher_role = factory.make_role_all_permissions("TE", self.course)
        factory.make_participation(teacher, self.course, teacher_role)
        factory.make_role('TA2', self.course)
        login = test.logging_in(self, teacher_user, teacher_pass)
        test.api_post_call(self, '/delete_course_role/', {'cID': 1, 'name': 'TA2'}, login)

        self.assertEquals(Role.objects.filter(name='TA2', course=Course.objects.get(pk=1)).count(), 0)
