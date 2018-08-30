"""
test_apis.py.

Test API calls.
"""
from django.test import TestCase
from VLE.models import Course, Assignment, Journal, Entry, Content, Comment

import VLE.factory as factory
import test.test_utils as test


class CreateApiTests(TestCase):
    def setUp(self):
        """Setup."""
        self.username, self.password, self.user = test.set_up_user_and_auth('test', 'test123', 'test@test.com')

    def test_create_new_course(self):
        """Test create new course."""
        username, password, user = test.set_up_user_and_auth('test2', 'test1233', 'test@ttaest.com', is_teacher=True)
        lti_id = '12AB'
        login = test.logging_in(self, username, password)
        create_course_dict = {'name': 'Beeldbewerken', 'abbr': 'BB', 'lti_id': lti_id}

        test.api_post_call(self, '/courses/', params=create_course_dict, logiin=login, status=201)
        self.assertEquals(Course.objects.get(lti_id=lti_id).name, 'Beeldbewerken')

    def test_create_new_assignment(self):
        """test create new assignment."""
        lti_id = '12AB'
        course = factory.make_course("BeeldBewerken", "BB")

        role = factory.make_role_default_no_perms("teacher", course, can_add_assignment=True)
        factory.make_participation(user=self.user, course=course, role=role)

        login = test.logging_in(self, self.username, self.password)
        create_assign_dict = {
            'name': 'SIFT',
            'description': 'In this assign...',
            'course_id': course.pk,
            'lti_id': lti_id
        }

        test.api_post_call(self, '/assignments/', params=create_assign_dict, login=login, status=201)
        self.assertEquals(Assignment.objects.get(lti_id=lti_id).name, 'SIFT')

    def test_create_journal(self):
        """test create journal."""
        assign = factory.make_assignment("Assignment", "Your favorite assignment")
        create_journal_dict = {'assignment_id': assign.pk}
        login = test.logging_in(self, self.username, self.password)

        course = factory.make_course("Portfolio Academische Vaardigheden", "PAV")
        assign.courses.add(course)

        role = factory.make_role_default_no_perms("student", course, can_edit_journal=True)
        factory.make_participation(user=self.user, course=course, role=role)

        test.api_post_call(self, '/journals/', params=create_journal_dict, login=login, status=201)
        self.assertTrue(Journal.objects.filter(user=self.user).exists())

    def test_create_entry(self):
        """"Test create entry."""
        assignment = factory.make_assignment("Assignment", "Your favorite assignment")
        journal = factory.make_journal(assignment, self.user)
        template = factory.make_entry_template("some_template")
        field = factory.make_field(template, 'Some field', 0)
        login = test.logging_in(self, self.username, self.password)

        create_entry_dict = {
            'journal_id': journal.id,
            'template_id': template.id,
            'content': [{
                'tag': field.pk,
                'data': "This is some data"
                }]
            }

        test.api_post_call(self, '/entries/', create_entry_dict, login, 201)
        self.assertTrue(Entry.objects.filter(node__journal=journal).exists())
        self.assertEquals(Content.objects.get(entry=1).data, "This is some data")

    def test_create_entrycomment(self):
        """Test create entry comment."""
        assignment = factory.make_assignment("Assignment", "Your favorite assignment")
        journal = factory.make_journal(assignment, self.user)
        template = factory.make_entry_template("some_template")
        entry = factory.make_entry(template)
        factory.make_node(journal, entry)

        login = test.logging_in(self, self.username, self.password)

        create_entrycomment_dict = {
            'entry_id': entry.pk,
            'user_id': self.user.pk,
            'text': 'Wow! This is bad/good',
            'published': True
        }

        test.api_post_call(self, '/comments/', params=create_entrycomment_dict, login=login, status=201)
        self.assertTrue(Comment.objects.filter(entry=entry).exists())
        self.assertEquals(Comment.objects.get(pk=1).text, 'Wow! This is bad/good')
