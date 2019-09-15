from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings
from django.db.models import Q

import VLE.lti_grade_passback as lti_grade
from VLE import factory
from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import Assignment, Comment, Entry, Journal


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

    for journal in Journal.objects.filter(assignment=assignment).exclude(Q(sourcedid=None) | Q(grade_url=None)):
        lti_grade.replace_result(journal)


@shared_task
def send_journal_grade_to_LMS(journal_pk):
    """Sends the grade of a journal to the LMS

    Reflags all journal entries to status needs grading
    If the grade update was succesfull, all entries are reflagged to grade update finished.

    Task results (or errors) are logged as a result string"""
    journal = Journal.objects.get(pk=journal_pk)

    if journal.sourcedid is None or journal.grade_url is None:
        return "This journal has no sourcedid: {} or grade_url: {}, skipping".format(
            journal.sourcedid, journal.grade_url)

    # Reflag -> all entries grade needs to be submitted to LMS
    Entry.objects.filter(grade__published=True, node__journal=journal).update(vle_coupling=Entry.GRADING)

    grade_request = GradePassBackRequest(settings.LTI_KEY, settings.LTI_SECRET, journal, send_score=True)
    response = grade_request.send_post_request()

    if response['code_mayor'] == 'success':
        # Reflag -> all entries grade (weighted avg) has been successfully submitted to LMS
        Entry.objects.filter(grade__published=True, node__journal=journal).update(vle_coupling=Entry.LINK_COMPLETE)
        return "Journal {} grade was succesfully sent to the LMS".format(journal_pk)

    return "Journal {} grade could not be sent to the LMS. Response was: {}".format(journal_pk, response)
