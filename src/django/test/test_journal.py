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
        self.ap = factory.AssignmentParticipation(assignment=self.group_assignment)
        self.g_student = self.ap.user
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

    def test_create_journal(self):
        payload = {'pk': self.group_journal.pk, 'assignment_id': self.group_assignment.pk, 'max_users': 3, 'amount': 2}
        before_count = Journal.objects.filter(assignment=self.group_assignment).count()

        # Check invalid users
        api.create(self, 'journals', params=payload, user=self.g_student, status=403)
        api.create(self, 'journals', params=payload, user=self.teacher, status=403)

        # Check valid creation of 2 journals
        api.create(self, 'journals', params=payload, user=self.g_teacher)

        # Check invalid amount
        payload['amount'] = 0
        api.create(self, 'journals', params=payload, user=self.g_teacher, status=400)

        after_count = Journal.objects.filter(assignment=self.group_assignment).count()

        assert before_count + 2 == after_count, '2 new journals should be added'
        assert Journal.objects.filter(assignment=self.group_assignment).last().max_users == 3, \
            'Journal should have the proper max amount of users'

    def test_update_journal(self):
        # Check if students need to specify a name to update journals
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.student, status=400)
        # Check teacher can always update name
        api.update(self, 'journals', params={'pk': self.journal.pk, 'name': 'new name'}, user=self.teacher)
        assert Journal.objects.get(pk=self.journal.pk).name == 'new name'

        # Check student can only update name if assignment allows
        api.update(self, 'journals', params={'pk': self.journal.pk, 'name': 'new name'}, user=self.student, status=403)
        self.assignment.can_set_journal_name = True
        self.assignment.save()
        api.update(self, 'journals', params={'pk': self.journal.pk, 'name': 'student name'}, user=self.student)
        assert Journal.objects.get(pk=self.journal.pk).name == 'student name'

        # Check teacher can update max_users only for group assignment
        api.update(self, 'journals', params={'pk': self.journal.pk, 'max_users': 4}, user=self.teacher, status=400)
        api.update(self, 'journals', params={'pk': self.group_journal.pk, 'max_users': 4}, user=self.g_teacher)
        assert Journal.objects.get(pk=self.group_journal.pk).max_users == 4
        # Check teacher cannot update max_users when there are more student in journal
        self.group_journal.authors.add(factory.AssignmentParticipation(assignment=self.group_assignment))
        self.group_journal.authors.add(factory.AssignmentParticipation(assignment=self.group_assignment))
        self.group_journal.authors.add(factory.AssignmentParticipation(assignment=self.group_assignment))
        api.update(
            self, 'journals', params={'pk': self.group_journal.pk, 'max_users': 1}, user=self.g_teacher, status=400)
        # Check teacher can update name and max_users

        api.update(
            self, 'journals', params={'pk': self.group_journal.pk, 'max_users': 9, 'name': 'NEW'}, user=self.g_teacher)
        journal = Journal.objects.get(pk=self.group_journal.pk)
        assert journal.max_users == 9 and journal.name == 'NEW'

        # Check if teacher can only update the published state
        api.update(self, 'journals', params={'pk': self.journal.pk}, user=self.teacher, status=400)
        api.update(self, 'journals', params={'pk': self.journal.pk, 'published': True}, user=self.teacher)

        # Check if the admin can update the journal
        api.update(self, 'journals', params={'pk': self.journal.pk, 'user': factory.Student().pk}, user=factory.Admin())

    def test_join(self):
        assert not self.group_journal.authors.filter(user=self.g_student).exists(), \
            'Check if student is not yet in the journal'
        api.update(self, 'journals/join', params={'pk': self.group_journal.pk}, user=self.g_student)
        assert self.group_journal.authors.filter(user=self.g_student).exists(), \
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

    def test_leave(self):
        self.group_journal.authors.add(self.ap)
        self.group_journal.save()

        assert self.group_journal.authors.filter(user=self.g_student).exists(), \
            'Check if student is added to the journal'
        api.update(self, 'journals/leave', params={'pk': self.group_journal.pk}, user=self.g_student)
        assert not self.group_journal.authors.filter(user=self.g_student).exists(), \
            'Check if student is not yet in the journal'

        # Check not in journal
        api.update(self, 'journals/leave', params={'pk': self.group_journal.pk}, user=self.g_student, status=400)
        # check not possible to leave non group assignment
        api.update(self, 'journals/leave', params={'pk': self.journal.pk}, user=self.student, status=400)
        # Check leave locked journal
        self.group_journal.authors.add(self.ap)
        self.group_journal.locked = True
        self.group_journal.save()
        api.update(self, 'journals/leave', params={'pk': self.group_journal.pk}, user=self.g_student, status=400)

    def test_kick(self):
        self.group_journal.authors.add(self.ap)
        self.group_journal.save()

        assert self.group_journal.authors.filter(user=self.g_student).exists(), \
            'Check if student is added to the journal'
        api.update(self, 'journals/kick', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
                   user=self.g_teacher)
        assert not self.group_journal.authors.filter(user=self.g_student).exists(), \
            'Check if student is not yet in the journal'

        # Check not in journal
        api.update(self, 'journals/kick', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
                   user=self.g_teacher, status=400)
        self.group_journal.authors.add(self.ap)
        self.group_journal.locked = True
        self.group_journal.save()
        # check not possible to kick from non group assignment
        api.update(self, 'journals/kick', params={'pk': self.journal.pk, 'user_id': self.student.pk},
                   user=self.teacher, status=400)
        # Check student cannot kick others
        api.update(self, 'journals/kick', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
                   user=factory.AssignmentParticipation(assignment=self.group_assignment).user, status=403)
        # Check kick locked journal
        api.update(self, 'journals/kick', params={'pk': self.group_journal.pk, 'user_id': self.g_student.pk},
                   user=self.g_teacher)

    def test_lock(self):
        self.group_journal.authors.add(self.ap)
        self.group_journal.save()

        api.update(self, 'journals/lock', params={
                'pk': self.group_journal.pk,
                'locked': True
            }, user=self.g_student)
        assert Journal.objects.get(pk=self.group_journal.pk).locked, \
            'Should be locked after student locks'
        api.update(self, 'journals/lock', params={
                'pk': self.group_journal.pk,
                'locked': False
            }, user=self.g_student)
        assert not Journal.objects.get(pk=self.group_journal.pk).locked, \
            'Should be unlocked after student unlocks'

        self.group_assignment.can_lock_journal = False
        self.group_assignment.save()
        api.update(self, 'journals/lock', params={
                'pk': self.group_journal.pk,
                'locked': True
            }, user=self.g_student, status=400)
        assert not Journal.objects.get(pk=self.group_journal.pk).locked, \
            'Should still be unlocked after failed attempt at locking'

        api.update(self, 'journals/lock', params={
                'pk': self.group_journal.pk,
                'locked': True
            }, user=self.g_teacher)
        assert Journal.objects.get(pk=self.group_journal.pk).locked, \
            'Teacher should sitll be able to lock journal'
