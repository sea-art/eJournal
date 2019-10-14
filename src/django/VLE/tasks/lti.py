from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import Entry, Node


@shared_task
def needs_grading(node_pk):
    """Give the teacher a needs grading notification in lti instance."""
    node = Node.objects.get(pk=node_pk)

    journal = node.journal
    course = node.journal.assignment.courses.order_by('-startdate').first()

    result_data = {'url': '{0}/Home/Course/{1}/Assignment/{2}/Journal/{3}?nID={4}'.format(
        settings.BASELINK, course.pk, journal.assignment.pk, journal.pk, node.pk)}

    for author in journal.authors:
        grade_request = GradePassBackRequest(author, journal.get_grade(),
                                             result_data=result_data, submitted_at=str(node.entry.last_edited))

        response = grade_request.send_post_request()
        if response['code_mayor'] == 'success':
            node.entry.vle_coupling = Entry.SEND_SUBMISSION
            node.entry.save()
        else:
            return False

    return True
