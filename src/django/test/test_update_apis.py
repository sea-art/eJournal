from django.test import TestCase

from VLE.models import Participation, Course, User, Role, Entry, Assignment
import VLE.serializers as serialize

import VLE.factory as factory
import test.test_utils as test


class UpdateApiTests(TestCase):
    def setUp(self):
        """Setup"""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123')
        self.course = factory.make_course("Beeldbewerken", "BB")

    def test_update_user_role_course(self):
        """Test user role update in a course."""
        login = test.logging_in(self, self.username, self.password)
        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")

        ta_role = factory.make_role_ta(name='TA', course=course)
        student_role = factory.make_role_student(name='SD', course=course)

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
        factory.make_role_student(name='Student', course=course)
        teacher_role = factory.make_role_teacher('Teacher', course)

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
        teacher_user, teacher_pass, teacher = test.set_up_user_and_auth('Teacher', 'pass')
        teacher_role = factory.make_role_teacher("TE", self.course)

        factory.make_role_ta('TA2', self.course)
        factory.make_participation(teacher, self.course, teacher_role)

        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_get_call(self, '/api/get_course_roles/1/', login)

        roles = result.json()['roles']
        for role in roles:
            if role['name'] == 'TA2':
                role['permissions']['can_grade_journal'] = 1

        roles.append(serialize.role_to_dict(factory.make_role_default_no_perms('test_role', self.course)))
        test.api_post_call(self, '/api/update_course_roles/', {'cID': 1, 'roles': roles}, login)

        role_test = Role.objects.get(name='TA2', course=self.course)
        self.assertTrue(role_test.can_grade_journal)
        self.assertEquals(Role.objects.filter(name='test_role', course=self.course).count(), 1)

    def test_update_assignment(self):
        """Test update assignment"""
        teacher_user, teacher_pass, teacher = test.set_up_user_and_auth('Teacher', 'pass')
        teacher_role = factory.make_role_all_permissions("TE", self.course)

        factory.make_participation(teacher, self.course, teacher_role)
        assign = test.set_up_assignments('Assign', '', 1, self.course)[0]

        login = test.logging_in(self, teacher_user, teacher_pass)

        test.api_post_call(self,
                           '/api/update_assignment/',
                           {'aID': assign.pk,
                            'name': 'Assign2',
                            'description': 'summary'},
                           login)

        assign = Assignment.objects.get(pk=assign.pk)
        self.assertEquals(assign.name, 'Assign2')
        self.assertEquals(assign.description, 'summary')

    def test_grade_publish(self):
        """Test the grade publish api functions."""
        teacher_user, teacher_pass, teacher = test.set_up_user_and_auth('Teacher', 'pass')
        students = test.set_up_users('student', 2)
        course1 = factory.make_course("BeeldBewerken", "BB", author=teacher)
        course2 = factory.make_course("Portfolio Academische Vaardigheden", "PAV", author=teacher)

        template = factory.make_entry_template('template_test')
        format = factory.make_format([template], 5)
        assign1 = factory.make_assignment("Colloq", "In de opdracht...1", teacher,
                                          format=format, courses=[course1, course2])
        journal1 = factory.make_journal(assign1, students[0])
        journal2 = factory.make_journal(assign1, students[1])
        entries = test.set_up_entries(template, 4)

        factory.make_node(journal1, entries[0])
        factory.make_node(journal1, entries[1])
        factory.make_node(journal1, entries[2])
        factory.make_node(journal2, entries[3])

        login = test.logging_in(self, teacher_user, teacher_pass)
        result = test.api_post_call(self, '/api/update_grade_entry/1/', {'grade': 1, 'published': 0}, login)
        self.assertEquals(Entry.objects.get(pk=1).grade, int(result.json()['new_grade']))

        result = test.api_post_call(self, '/api/update_grade_entry/1/', {'grade': 2, 'published': 1}, login)
        self.assertEquals(Entry.objects.get(pk=1).grade, int(result.json()['new_grade']))
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))

        result = test.api_post_call(self, '/api/update_publish_grade_entry/1/', {'published': 0}, login)
        self.assertEquals(Entry.objects.get(pk=1).published, int(result.json()['new_published']))

        for i in range(2, 4):
            test.api_post_call(self, '/api/update_grade_entry/{}/'.format(i + 1), {'grade': 1, 'published': 0}, login)
        result = test.api_post_call(self, '/api/update_publish_grades_assignment/1/', {'published': 1}, login)
        self.assertEquals(Entry.objects.filter(node__journal__assignment=assign1, published=1).count(), 3)

        result = test.api_post_call(self, '/api/update_publish_grades_journal/1/', {'published': 0}, login)
        self.assertEquals(Entry.objects.filter(node__journal=1, published=0).count(), 3)
        self.assertEquals(Entry.objects.get(pk=4).published, 1)

    def test_update_password(self):
        """Test update assignment"""
        login = test.logging_in(self, self.username, self.password)

        test.api_post_call(self,
                           '/api/update_password/',
                           {'new_password': 'Pass123!',
                            'old_password': self.password},
                           login)

        test.logging_in(self, self.username, 'Pass123!')

        test.api_post_call(self,
                           '/api/update_password/',
                           {'new_password': 'Pass123!',
                            'old_password': self.password},
                           login)
