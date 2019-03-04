from __future__ import absolute_import, unicode_literals

from celery import shared_task

import VLE.lti_grade_passback as lti_grade
from VLE.models import Assignment, Comment, Entry


@shared_task
def publish_all_assignment_grades(assignment_pk, published):
    """Publish all grades that are not None for an assignment.

    - assignment: the assignment in question
    - published: either True or False. If True show the grade to student.
    """
    assignment = Assignment.objects.get(pk=assignment_pk)

    Entry.objects.filter(node__journal__assignment=assignment).exclude(grade=None).update(published=published)
    if published:
        Comment.objects.filter(entry__node__journal__assignment=assignment) \
                       .exclude(entry__grade=None).update(published=True)
        for journal in assignment.journal_set.all():
            if journal.sourcedid is not None and journal.grade_url is not None:
                lti_grade.replace_result(journal)
