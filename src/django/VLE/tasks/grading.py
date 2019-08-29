from __future__ import absolute_import, unicode_literals

from celery import shared_task

import VLE.lti_grade_passback as lti_grade
from VLE import factory
from VLE.models import Assignment, Comment, Entry


@shared_task
def publish_all_assignment_grades(user, assignment_pk):
    """Publish all grades that are not None for an assignment.

    - assignment: the assignment in question
    """
    assignment = Assignment.objects.get(pk=assignment_pk)

    entries = Entry.objects.filter(node__journal__assignment=assignment).exclude(grade=None)

    for entry in entries:
        factory.make_grade(entry, user.pk, entry.grade.grade, True)

    Comment.objects.filter(entry__node__journal__assignment=assignment) \
                   .exclude(entry__grade=None).update(published=True)
    for journal in assignment.journal_set.all():
        if journal.sourcedid is not None and journal.grade_url is not None:
            lti_grade.replace_result(journal)
