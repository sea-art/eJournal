import test.factory as factory
from test.utils import api

from django.test import TestCase


class JournalAPITest(TestCase):
    def setUp(self):
        self.journal = factory.Journal()
        self.student = self.journal.authors.first().user
        self.assignment = self.journal.assignment
        self.course = self.assignment.courses.first()
        self.teacher = self.course.author

        self.group_assignment = factory.GroupAssignment()
        self.group_journal = factory.GroupJournal(assignment=self.group_assignment)
        ap = factory.AssignmentParticipation(assignment=self.group_assignment)
        self.group_student = ap.user
        self.group_course = self.group_assignment.courses.first()
        self.group_teacher = self.group_course.author

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
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.group_student)
