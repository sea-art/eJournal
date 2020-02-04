from __future__ import absolute_import, unicode_literals

from celery import shared_task

import VLE.lti_grade_passback as lti_grade
from VLE.models import Entry, Journal, Node
from VLE.tasks.lti import needs_grading as needs_grading_task


@shared_task
def check_if_need_VLE_publish():
    for node in Node.objects.filter(
        entry__vle_coupling=Entry.NEED_SUBMISSION,
        journal__sourcedid__isnull=False,
        journal__user__participation__role__can_have_journal=True
    ):
        # Filter out any journals that are filtered with the journal queryset
        if Journal.objects.filter(pk=node.journal.pk).exists():
            needs_grading_task(node.pk)
    for journal in Entry.objects.filter(
        vle_coupling=Entry.GRADING,
        grade__published=True,
        node__journal__user__participation__role__can_have_journal=True
    ).values('node__journal').distinct():
        # Filter out any journals that are filtered with the journal queryset
        journal = Journal.objects.filter(pk=journal['node__journal']).first()
        if journal is not None:
            lti_grade.replace_result(journal)
