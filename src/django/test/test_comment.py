import random
import string
import test.factory as factory
from test.utils import api

from django.test import TestCase

import VLE.factory as nfac
from VLE.models import Comment


def set_entry_comment_counts(obj):
    obj.entry_comments = Comment.objects.filter(entry=obj.comment.entry).count()
    obj.entry_published_comments = Comment.objects.filter(entry=obj.comment.entry, published=True).count()
    obj.entry_unpublished_comments = obj.entry_comments - obj.entry_published_comments


def assert_comments_are_equal(c1, c2):
    assert c1.pk == c2.pk, 'Primary keys are not equal'
    assert c1.text == c2.text, 'Texts are not equal'
    assert c1.creation_date == c2.creation_date, 'Creation dates are not equal'
    assert c1.last_edited == c2.last_edited, 'Last editeds are not equal'
    assert c1.last_edited_by == c2.last_edited_by, 'Last edited bys are not equal'


class CommentAPITest(TestCase):
    def setUp(self):
        self.admin = factory.Admin()
        self.journal = factory.Journal()
        self.student = self.journal.authors.first().user
        self.TA = factory.Student()
        nfac.make_participation(
            user=self.TA,
            course=self.journal.assignment.courses.first(),
            role=self.journal.assignment.courses.first().role_set.get(name='TA')
        )
        self.teacher = self.journal.assignment.courses.first().author
        self.comment = factory.StudentComment(entry__node__journal=self.journal)
        self.TA_comment = nfac.make_comment(self.comment.entry, self.TA, 'TA comment', False)
        self.teacher_comment = nfac.make_comment(self.comment.entry, self.teacher, 'Teacher comment', False)
        set_entry_comment_counts(self)

        assert self.teacher.has_permission('can_grade', self.journal.assignment), \
            'Teacher requires can_grade permission in the relevant assignment'
        assert self.TA.has_permission('can_grade', self.journal.assignment), \
            'TA requires can_grade permission in the relevant assignment'
        assert not self.teacher_comment.published, 'Teacher comment should be unpublished.'
        assert not self.TA_comment.published, 'TA comment should be unpublished.'
        assert self.entry_comments == 3, 'Journal should have 3 comments total'
        assert self.entry_published_comments == 1, 'Journal should have 3 comments of which only one is published'
        assert self.entry_unpublished_comments == 2, 'Expected 2 unpublished comments'

    def test_get(self):
        comments = api.get(
            self, 'comments', params={'entry_id': self.teacher_comment.entry.pk}, user=self.student)['comments']
        assert len(comments) == self.entry_published_comments, 'Student can only see published comments'

        api.get(self, 'comments', params={'pk': self.teacher_comment.pk}, user=self.student, status=403)
        api.get(self, 'comments', params={'pk': self.teacher_comment.pk}, user=self.teacher)

        comments = api.get(self, 'comments', params={'entry_id': self.comment.entry.pk}, user=self.teacher)['comments']
        assert len(comments) == self.entry_comments, 'Teacher should be able to see all comments'

        self.teacher_comment.published = True
        self.teacher_comment.save()
        self.entry_published_comments = self.entry_published_comments + 1
        self.entry_unpublished_comments = self.entry_unpublished_comments - 1

        comments = api.get(
            self, 'comments', params={'entry_id': self.teacher_comment.entry.pk}, user=self.student)['comments']
        assert len(comments) == self.entry_published_comments, 'Student should be able to see published comments'

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

        set_entry_comment_counts(self)

    def test_update_as_admin(self):
        # Admin should be allowed to edit a teachers comment
        self.check_comment_update(self.teacher_comment, self.admin, True)
        # Admin should be allowed to edit students comment
        self.check_comment_update(self.comment, self.admin, True)
        # Admin should be allowed to edit TA comment
        self.check_comment_update(self.TA_comment, self.admin, True)

    def test_update_as_teacher(self):
        # Teacher should be allowed to edit his own comment
        self.check_comment_update(self.teacher_comment, self.teacher, True)
        # Teacher should not be allowed to edit students comment
        self.check_comment_update(self.comment, self.teacher, False)
        # Teacher should be allowed to edit TA comment
        self.check_comment_update(self.TA_comment, self.teacher, True)

    def test_update_as_TA(self):
        # TA should be allowed to edit his own comment
        self.check_comment_update(self.TA_comment, self.TA, True)
        # TA should not be allowed to edit a students comment
        self.check_comment_update(self.comment, self.TA, False)
        # TA should not be allowed to edit a Teachers comment
        self.check_comment_update(self.teacher_comment, self.TA, False)

        TA_role = self.journal.assignment.courses.first().role_set.get(name='TA')
        TA_role.can_edit_staff_comment = True
        TA_role.save()
        # TA with 'can_edit_staff_comment' should be allowed to edit his own comment
        self.check_comment_update(self.TA_comment, self.TA, True)
        # TA with 'can_edit_staff_comment' should not be allowed to edit a students comment
        self.check_comment_update(self.comment, self.TA, False)
        # TA with 'can_edit_staff_comment' should be allowed to edit a Teachers comment
        self.check_comment_update(self.teacher_comment, self.TA, True)
        TA_role.can_edit_staff_comment = False
        TA_role.save()

    def test_update_as_student(self):
        # Student should be allowed to edit his own comment
        self.check_comment_update(self.comment, self.student, True)
        # Student should not be allowed to edit a TA's comment
        self.check_comment_update(self.TA_comment, self.student, False)
        # Student should not be allowed to edit a Teachers comment
        self.check_comment_update(self.teacher_comment, self.student, False)

    def test_delete_as_admin(self):
        # Admin should be allowed to delete a teachers comment
        self.check_comment_delete(self.teacher_comment, self.admin, True)
        # Admin should be allowed to delete students comment
        self.check_comment_delete(self.comment, self.admin, True)
        # Admin should be allowed to delete TA comment
        self.check_comment_delete(self.TA_comment, self.admin, True)

    def test_delete_as_teacher(self):
        # Teacher should be allowed to delete his own comment
        self.check_comment_delete(self.teacher_comment, self.teacher, True)
        # Teacher should not be allowed to delete students comment
        self.check_comment_delete(self.comment, self.teacher, False)
        # Teacher should be allowed to delete TA comment
        self.check_comment_delete(self.TA_comment, self.teacher, True)

    def test_delete_as_TA(self):
        # TA should be allowed to delete his own comment
        self.check_comment_delete(self.TA_comment, self.TA, True)
        # TA should not be allowed to delete a students comment
        self.check_comment_delete(self.comment, self.TA, False)
        # TA should not be allowed to delete a Teachers comment
        self.check_comment_delete(self.teacher_comment, self.TA, False)

        TA_role = self.journal.assignment.courses.first().role_set.get(name='TA')
        TA_role.can_edit_staff_comment = True
        TA_role.save()
        # TA with 'can_edit_staff_comment' should be allowed to delete his own comment
        self.check_comment_delete(self.TA_comment, self.TA, True)
        # TA with 'can_edit_staff_comment' should not be allowed to delete a students comment
        self.check_comment_delete(self.comment, self.TA, False)
        # TA with 'can_edit_staff_comment' should be allowed to delete a Teachers comment
        self.check_comment_delete(self.teacher_comment, self.TA, True)
        self.journal.assignment.courses.first().role_set.filter(
            name='TA').update(can_edit_staff_comment=False)

    def test_delete_as_student(self):
        # Student should be allowed to delete his own comment
        self.check_comment_delete(self.comment, self.student, True)
        # Student should not be allowed to delete a TA's comment
        self.check_comment_delete(self.TA_comment, self.student, False)
        # Student should not be allowed to delete a Teachers comment
        self.check_comment_delete(self.teacher_comment, self.student, False)

    def check_comment_update(self, comment, user, should_succeed):
        update_msg = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(50))
        comment_before_op = Comment.objects.get(pk=comment.pk)

        if should_succeed:
            old_comment_resp = api.get(self, 'comments', params={'pk': comment.pk}, user=user)['comment']

        comment_resp = api.update(
            self,
            'comments',
            params={'pk': comment.pk, 'text': update_msg},
            user=user,
            status=200 if should_succeed else 403
        )

        comment_after_op = Comment.objects.get(pk=comment.pk)

        if should_succeed:
            comment_resp = comment_resp['comment']
            assert comment_resp['text'] == update_msg, 'Text should be updated'
            assert comment_resp['creation_date'] == old_comment_resp['creation_date'], 'Creation date modified'
            assert comment_resp['last_edited'] != old_comment_resp['last_edited'], 'Last edited not updated'
            assert comment_resp['last_edited_by'] == user.full_name, 'Last edited by incorrect'
        else:
            assert_comments_are_equal(comment_before_op, comment_after_op)

    def check_comment_delete(self, comment, user, should_succeed):
        comment_before_op = Comment.objects.get(pk=comment.pk)

        api.delete(self, 'comments', params={'pk': comment.pk}, user=user, status=200 if should_succeed else 403)

        if should_succeed:
            assert not Comment.objects.filter(pk=comment.pk).exists(), 'Comment was not succesfully deleted'
            comment_before_op.save()
        else:
            comment_after_op = Comment.objects.get(pk=comment.pk)
            assert_comments_are_equal(comment_before_op, comment_after_op)
