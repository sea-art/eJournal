from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import AssignmentParticipation, Entry, Journal, Node
from VLE.utils import grading


@shared_task
def needs_grading(node_pk):
    """Give the teacher a needs grading notification in lti instance."""
    node = Node.objects.get(pk=node_pk)

    journal = node.journal
    responses = {}
    failed = False
    for author in journal.authors.all():
        course = journal.assignment.get_active_course(author.user)
        result_data = {
            'url': '{0}/Home/Course/{1}/Assignment/{2}/Journal/{3}?nID={4}'.format(
                settings.BASELINK, course.pk, journal.assignment.pk, journal.pk, node.pk)
        }
        grade_request = GradePassBackRequest(author, journal.get_grade(),
                                             result_data=result_data, submitted_at=str(node.entry.last_edited))

        responses[author.pk] = grade_request.send_post_request()
        if responses[author.pk]['code_mayor'] != 'success':
            failed = True

    if not failed:
        node.entry.vle_coupling = Entry.SENT_SUBMISSION
        node.entry.save()

    return responses


@shared_task
def left_journal_passback(author_pk, journal_pk):
    journal = Journal.objects.get(pk=journal_pk)
    author = AssignmentParticipation.objects.get(pk=author_pk)
    return grading.send_grade_to_LMS(journal, author, left_journal=True)


@shared_task
def join_journal_passback(author_pk, journal_pk):
    journal = Journal.objects.get(pk=journal_pk)
    author = AssignmentParticipation.objects.get(pk=author_pk)
    return grading.send_grade_to_LMS(journal, author)
