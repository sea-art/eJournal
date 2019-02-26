import test.factory as factory
from test.utils import api

from django.test import TestCase


class NodeAPITest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        self.journal = factory.Journal(user=self.student)
        self.teacher = self.journal.assignment.courses.first().author
        self.comment = factory.StudentComment(entry__node__journal=self.journal)
        self.teacher_comment = factory.TeacherComment(entry__node__journal=self.journal)

    def test_get(self):
        comments = api.get(
            self, 'comments', params={'entry_id': self.teacher_comment.entry.pk}, user=self.student)['comments']
        assert len(comments) == 0, 'Student should not be able to see unpublished comments'

        api.get(self, 'comments', params={'pk': self.teacher_comment.pk}, user=self.student, status=403)
        api.get(self, 'comments', params={'pk': self.teacher_comment.pk}, user=self.teacher)

        comments = api.get(self, 'comments', params={'entry_id': self.comment.entry.pk}, user=self.teacher)['comments']
        assert len(comments) == 1, 'Teacher should be able to see unpublished comments'

        self.teacher_comment.published = True
        self.teacher_comment.save()
        comments = api.get(
            self, 'comments', params={'entry_id': self.teacher_comment.entry.pk}, user=self.student)['comments']
        assert len(comments) == 1, 'Student should be able to see published comments'

        api.get(self, 'comments', params={'entry_id': self.comment.entry.pk}, user=factory.Student(), status=403)
        api.get(self, 'comments', params={'entry_id': self.comment.entry.pk}, user=factory.Admin())

    def test_create(self):
        api.create(self, 'comments',
                   params={'entry_id': self.comment.entry.pk, 'text': 'test-create-comment'},
                   user=self.student)

        comment = api.create(
            self, 'comments',
            params={'entry_id': self.comment.entry.pk, 'text': 'test-create-comment', 'published': False},
            user=self.student)['comment']
        assert comment['published'], 'Student should not be able to post unpublished comments'

        comment = api.create(
            self, 'comments',
            params={'entry_id': self.comment.entry.pk, 'text': 'test-create-comment', 'published': False},
            user=self.teacher)['comment']
        assert not comment['published'], 'Comment should not be published'

        comment = api.create(
            self, 'comments',
            params={'entry_id': self.comment.entry.pk, 'text': 'test-create-comment', 'published': True},
            user=self.teacher)['comment']
        assert comment['published'], 'Comment should be published'

        api.create(
            self, 'comments',
            params={'entry_id': self.comment.entry.pk, 'text': 'test-create-comment', 'published': True},
            user=factory.Student(), status=403)

    def test_update(self):
        self.comment.published = True
        self.comment.save()

        # Teacher should not be allowed to edit students comment
        api.update(self, 'comments', params={'pk': self.comment.pk, 'text': 'test-update-comment'},
                   user=self.teacher, status=403)

        old_comment = api.get(self, 'comments', params={'pk': self.comment.pk}, user=self.student)['comment']
        comment = api.update(self, 'comments', params={'pk': self.comment.pk, 'text': 'test-update-comment'},
                             user=self.student)['comment']
        assert comment['text'] == 'test-update-comment', 'Text should be updated'
        assert comment['creation_date'] == old_comment['creation_date']
        assert comment['last_edited'] != old_comment['last_edited']

        api.update(self, 'comments', params={'pk': self.teacher_comment.pk, 'text': 'test-update-comment'},
                   user=self.teacher)

    def test_delete(self):
        api.delete(self, 'comments', params={'pk': self.comment.pk}, user=self.teacher, status=403)
        api.delete(self, 'comments', params={'pk': self.comment.pk}, user=self.student)
        api.delete(self, 'comments', params={'pk': self.teacher_comment.pk}, user=factory.Admin())
