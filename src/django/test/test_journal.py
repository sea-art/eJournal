import test.factory as factory
from test.utils import api

from django.test import TestCase


class JournalAPITest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        self.journal = factory.Journal(user=self.student)
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

    def test_list_journal(self):
        assignment = factory.Assignment()
        course1 = assignment.courses.first()
        factory.Journal(assignment=assignment)
        course2 = factory.Course()
        assignment.courses.add(course2)
        factory.Journal(assignment=assignment)

        result = api.get(
            self, 'journals', params={'assignment_id': assignment.pk, 'course_id': course2.pk}, user=course2.author)
        assert len(result['journals']) == 1, 'Course2 is supplied, only journals from that course should appear (1)'

        result = api.get(
            self, 'journals', params={'assignment_id': assignment.pk}, user=self.teacher, status=400)

        result = api.get(
            self, 'journals', params={'assignment_id': assignment.pk, 'course_id': course1.pk}, user=course1.author)
        assert len(result['journals']) == 2, 'Course1 is supplied, only journals from that course should appear (2)'

        # Should not work when user is not in supplied course
        result = api.get(
            self, 'journals', params={'assignment_id': assignment.pk, 'course_id': course1.pk}, user=course2.author,
            status=403)

    def test_update(self):
        # Check if students cannot update journals
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.student, status=403)

        # Check if teacher can only update the published state
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.teacher, status=403)
        api.update(self, 'journals', params={'pk': self.journal.pk, 'published': True}, user=self.teacher)

        # Check if the admin can update the journal
        api.update(self, 'journals', params={'pk': self.journal.pk, 'user': factory.Student().pk}, user=factory.Admin())
