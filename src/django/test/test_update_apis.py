from django.test import TestCase

from VLE.models import Participation, Course, User, Role
import VLE.serializers as serialize

import VLE.factory as factory
import test.test_rest as test


class UpdateApiTests(TestCase):
    def setUp(self):
        """Setup"""
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)
        self.course = factory.make_course("Beeldbewerken", "BB")

    def test_update_user_role_course(self):
        """Test user role update in a course."""
        login = test.logging_in(self, self.username, self.password)
        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        ta_role = factory.make_role(name='TA', course=course, can_grade_journal=True,
                                    can_view_assignment_participants=True)
        student_role = factory.make_role(name='SD', course=course, can_edit_journal=True, can_comment_journal=True)

        self.user_role = factory.make_user("test123", "test")
        factory.make_participation(self.user_role, course, ta_role)
        factory.make_participation(self.user, course, student_role)

        user_role = Participation.objects.get(user=self.user_role, course=2).role.name
        self.assertEquals(user_role, 'TA')

        test.api_post_call(
            self,
            '/api/update_user_role_course/',
            {'cID': 2, 'uID': self.user_role.pk, 'role': 'SD'},
            login
        )
        user_role = Participation.objects.get(user=self.user_role, course=2).role.name
        self.assertEquals(user_role, 'SD')

    def test_update_course(self):
        """Test update_course"""

        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        test.api_post_call(
            self,
            '/api/update_course/',
            {'cID': course.pk, 'name': 'Beeldbewerken', 'abbr': 'BB', 'startDate': course.startdate},
            login
        )

        course = Course.objects.get(pk=course.pk)
        self.assertEquals(course.name, 'Beeldbewerken')
        self.assertEquals(course.abbreviation, 'BB')

    def test_update_course_with_studentID(self):
        """Test update_course_with_studentID"""

        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        factory.make_role(name='Student', course=course, can_edit_journal=True, can_comment_journal=True)
        teacher_role = factory.make_role_all_permissions('Teacher', course)

        factory.make_participation(self.user, course, teacher_role)
        student = factory.make_user("Rick", "pass")

        test.api_post_call(
            self,
            '/api/update_course_with_studentID/',
            {'uID': student.pk, 'cID': course.pk},
            login
        )

        course = Course.objects.get(pk=course.pk)
        self.assertEquals(len(course.users.all()), 2)
        self.assertTrue(User.objects.filter(participation__course=course, username='Rick').exists())

    def test_update_course_roles(self):
        """Test update course roles"""
        factory.make_role('TA2', self.course)
        teacher_user = 'Teacher'
        teacher_pass = 'pass'
        teacher = factory.make_user(teacher_user, teacher_pass)
        teacher_role = factory.make_role_all_permissions("TE", self.course)
        factory.make_participation(teacher, self.course, teacher_role)
        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_get_call(self, '/api/get_course_roles/1/', login)
        roles = result.json()['roles']
        for role in roles:
            if role['name'] == 'TA2':
                role['permissions']['can_grade_journal'] = 1
        roles.append(serialize.role_to_dict(factory.make_role('test_role', self.course)))
        test.api_post_call(self, '/api/update_course_roles/', {'cID': 1, 'roles': roles}, login)
        role_test = Role.objects.get(name='TA2', course=self.course)

        self.assertTrue(role_test.can_grade_journal)
        self.assertEquals(Role.objects.filter(name='test_role', course=self.course).count(), 1)
