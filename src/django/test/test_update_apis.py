from django.test import TestCase

from VLE.models import Participation, Course, User

import VLE.factory as factory
import test.test_rest as test


class UpdateApiTests(TestCase):
    def setUp(self):
        """Setup"""
        self.username = 'test'
        self.password = 'test123'

        self.user = factory.make_user(self.username, self.password)

    def test_update_user_role_course(self):
        """Test user role update in a course."""
        login = test.logging_in(self, self.username, self.password)

        ta_role = factory.make_role(name='TA', can_grade_journal=True, can_view_assignment_participants=True)
        student_role = factory.make_role(name='SD', can_edit_journal=True, can_comment_journal=True)

        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        self.user_role = factory.make_user("test123", "test")
        factory.make_participation(self.user_role, course, ta_role)
        factory.make_participation(self.user, course, student_role)

        user_role = Participation.objects.get(user=self.user_role, course=1).role.name
        self.assertEquals(user_role, 'TA')

        test.api_post_call(
            self,
            '/api/update_user_role_course/',
            {'cID': 1, 'uID': self.user_role.pk, 'role': 'SD'},
            login
        )
        user_role = Participation.objects.get(user=self.user_role, course=1).role.name
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
        factory.make_role(name='Student', can_edit_journal=True, can_comment_journal=True)
        teacher_role = factory.make_role(name='Teacher', can_edit_course_roles=True, can_view_course_participants=True,
                                         can_edit_course=True, can_delete_course=True,
                                         can_add_assignment=True, can_view_assignment_participants=True,
                                         can_delete_assignment=True, can_publish_assigment_grades=True,
                                         can_grade_journal=True, can_publish_journal_grades=True,
                                         can_comment_journal=True)

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
