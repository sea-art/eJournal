from __future__ import absolute_import, unicode_literals

from celery import shared_task

import VLE.lti_grade_passback as lti_grade
from VLE.models import Entry, Journal, Node
from VLE.tasks.lti import needs_grading as needs_grading_task


@shared_task
def check_if_need_VLE_publish():
    # TODO: Check if "user__participation__role__can_have_journal" would not leak
    # if its a teacher and student in different courses
    for node in Node.objects.filter(
        entry__vle_coupling=Entry.NEED_SUBMISSION,
        journal__sourcedids__isnull=False,
        journal__authors__participation__role__can_have_journal=True
    ):
        # Question: Is not repeating code worth the extra get?
        needs_grading_task(node.pk)
    for journal in Entry.objects.filter(
        vle_coupling=Entry.GRADING,
        published=True,
        node__journal__authors__participation__role__can_have_journal=True
    ).values('node__journal').distinct():
        lti_grade.replace_result(Journal.objects.get(pk=journal['node__journal']))
