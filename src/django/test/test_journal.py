import test.factory as factory
from test.utils import api

from django.test import TestCase


class JournalAPITest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        self.journal = factory.Journal(authors=[self.student])
        self.assignment = self.journal.assignment
        self.course = self.assignment.courses.first()
        self.teacher = self.course.author

        self.group_journal = factory.GroupJournal(authors=[self.student])
        self.group_assignment = self.group_journal.assignment
        self.group_course = self.assignment.courses.first()
        self.group_teacher = self.course.author

    def test_get(self):
        payload = {'assignment_id': self.assignment.pk, 'course_id': self.course.pk}
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

    def test_join(self):
        student = factory.Participation(course=self.group_course).user
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=student)
