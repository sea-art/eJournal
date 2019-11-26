import test.factory as factory
from test.utils import api

from django.test import TestCase

from VLE.models import Journal


class JournalAPITest(TestCase):
    def setUp(self):
        self.journal = factory.Journal()
        self.student = self.journal.authors.first().user
        self.assignment = self.journal.assignment
        self.course = self.assignment.courses.first()
        self.teacher = self.course.author

        self.group_assignment = factory.GroupAssignment()
        self.group_journal = factory.GroupJournal(assignment=self.group_assignment)
        self.group_journal2 = factory.GroupJournal(assignment=self.group_assignment)
        ap = factory.AssignmentParticipation(assignment=self.group_assignment)
        self.g_student = ap.user
        group_course = self.group_assignment.courses.first()
        self.g_teacher = group_course.author

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
        # Check if students need to specify a name to update journals
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.student, status=400)

        # Check if teacher can only update the published state
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.teacher, status=400)
        api.update(self, 'journals', params={'pk': self.journal.pk, 'published': True}, user=self.teacher)

        # Check if the admin can update the journal
        api.update(self, 'journals', params={'pk': self.journal.pk, 'user': factory.Student().pk}, user=factory.Admin())

    def test_join(self):
        assert not Journal.objects.get(pk=self.group_journal.pk).authors.filter(user=self.g_student).exists(), \
            'Check if student is not yet in the journal'
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.g_student)
        assert Journal.objects.get(pk=self.group_journal.pk).authors.filter(user=self.g_student).exists(), \
            'Check if student is added to the journal'
        # Check already joined
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.g_student, status=400)
        # Check not in assignment
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=factory.Student(), status=403)
        # Check teacher is not able to join
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.g_teacher, status=403)
        # Check only 1 journal at the time
        api.update(self, 'journals/join', params={'pk': self.group_journal2.pk}, user=self.g_student, status=400)
        # Check max student
        for _ in range(self.group_journal2.max_users - self.group_journal2.authors.count()):
            api.update(
                self, 'journals/join', params={'pk': self.group_journal2.pk},
                user=factory.AssignmentParticipation(assignment=self.group_assignment).user)
        api.update(
            self, 'journals/join', params={'pk': self.group_journal2.pk},
            user=factory.AssignmentParticipation(assignment=self.group_assignment).user, status=400)

        # Check locked journal
        self.group_journal.locked = True
        self.group_journal.save()
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.g_student, status=400)

    def test_add_student(self):
        assert not Journal.objects.get(pk=self.group_journal.pk).authors.filter(user=self.g_student).exists(), \
            'Check if student is not yet in the journal'
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
            user=self.g_teacher)
        assert Journal.objects.get(pk=self.group_journal.pk).authors.filter(user=self.g_student).exists(), \
            'Check if student is added to the journal'
        # Check already joined
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
            user=self.g_teacher, status=400)
        # Check not in assignment
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal.pk, 'user_id': factory.Student().pk},
            user=self.g_teacher, status=403)
        # Check teacher is not able to join
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal.pk, 'user_id': self.g_teacher.pk},
            user=self.g_teacher, status=403)
        # Check only 1 journal at the time
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal2.pk, 'user_id': self.g_student.pk},
            user=self.g_teacher, status=400)
        # Check max student
        for _ in range(self.group_journal2.max_users - self.group_journal2.authors.count()):
            student = factory.AssignmentParticipation(assignment=self.group_assignment).user
            api.update(
                self, 'journals/add_student', params={'pk': self.group_journal2.pk, 'user_id': student.pk},
                user=self.g_teacher)
        student = factory.AssignmentParticipation(assignment=self.group_assignment).user
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal2.pk, 'user_id': student.pk},
            user=self.g_teacher, status=400)

        # Check if teacher can still add when it is a locked journal
        self.group_journal.locked = True
        self.group_journal.save()
        api.update(
            self, 'journals/add_student', params={'pk': self.group_journal.pk, 'user_id': student.pk},
            user=self.g_teacher)
