import test.factory as factory
from test.utils import api

from django.test import TestCase


class JournalAPITest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        self.journal = factory.Journal(authors=[self.student])
        self.teacher = self.journal.assignment.courses.first().author

    def test_get(self):
        assignment = self.journal.assignment
        course = assignment.courses.first()
        payload = {'assignment_id': assignment.pk, 'course_id': course.pk}
        # Test list
        api.get(self, 'journals', params=payload, user=self.student, status=403)
        api.get(self, 'journals', params=payload, user=self.teacher)

        # Test get
        api.get(self, 'journals', params={'pk': self.journal.pk}, user=self.student)
        api.get(self, 'journals', params={'pk': self.journal.pk}, user=self.teacher)
        api.get(self, 'journals', params={'pk': self.journal.pk}, user=factory.Teacher(), status=403)

    def test_update(self):
        # Check if students cannot update journals
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.student, status=403)

        # Check if teacher can only update the published state
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.teacher, status=403)
        api.update(self, 'journals', params={'pk': self.journal.pk, 'published': True}, user=self.teacher)

        # Check if the admin can update the journal
        api.update(self, 'journals', params={'pk': self.journal.pk, 'user': factory.Student().pk}, user=factory.Admin())
