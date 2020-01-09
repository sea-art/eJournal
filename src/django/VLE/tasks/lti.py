from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import AssignmentParticipation, Entry, Node


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
        node.entry.vle_coupling = Entry.SEND_SUBMISSION
        node.entry.save()

    return responses


@shared_task
def left_journal_passback(author_pk, node_pk):
    """Give the teacher a needs grading notification in lti instance."""
    node = Node.objects.get(pk=node_pk)

    journal = node.journal
    author = AssignmentParticipation.objects.get(pk=author_pk)

    course = journal.assignment.get_active_course(author.user)
    result_data = {
        'url': '{0}/Home/Course/{1}/Assignment/{2}/Journal/{3}?left=true'.format(
            settings.BASELINK, course.pk, journal.assignment.pk, journal.pk)
    }
    grade = journal.get_grade() if not journal.assignment.remove_grade_upon_leaving_group else 0
    grade_request = GradePassBackRequest(author, grade,
                                         result_data=result_data, submitted_at=str(node.entry.last_edited))

    return grade_request.send_post_request()
