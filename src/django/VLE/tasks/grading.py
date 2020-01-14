from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

import VLE.lti_grade_passback as lti_grade
from VLE import factory
from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import Assignment, AssignmentParticipation, Comment, Entry, Journal


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

    for journal in Journal.objects.filter(assignment=assignment).distinct():
        lti_grade.replace_result(journal)


@shared_task
def update_author_grade_to_LMS(author_pk, journal=None):
    """Sends the grade of an author to the LMS

    It sets the grade to 0 if no journal is found."""
    author = AssignmentParticipation.objects.get(pk=author_pk)
    if journal is None:
        journal = Journal.objects.filter(authors__in=[author]).first()

    if author.sourcedid is None:
        return "{} has no sourcedid".format(author.to_string(user=author.user))
    if author.grade_url is None:
        return "{} has no grade_url".format(author.to_string(user=author.user))

    if journal is not None:
        # Reflag -> all entries grade needs to be submitted to LMS
        Entry.objects.filter(grade__published=True, node__journal=journal).update(vle_coupling=Entry.GRADING)
        course = journal.assignment.get_active_course(author.user)
        result_data = {
            'url': '{0}/Home/Course/{1}/Assignment/{2}/Journal/{3}'.format(
                settings.BASELINK, course.pk, journal.assignment.pk, journal.pk)
        }
        grade_request = GradePassBackRequest(author, journal.get_grade(), result_data=result_data, send_score=True)
    else:
        grade_request = GradePassBackRequest(author, 0, send_score=True)

    response = grade_request.send_post_request()

    if response['code_mayor'] == 'success':
        # Reflag -> all entries grade (weighted avg) has been successfully submitted to LMS
        Entry.objects.filter(grade__published=True, node__journal=journal).update(vle_coupling=Entry.LINK_COMPLETE)

    return response


@shared_task
def send_journal_grade_to_LMS(journal_pk):
    """Sends the grade of a journal to the LMS

    Reflags all journal entries to status needs grading
    If the grade update was succesfull, all entries are reflagged to grade update finished.

    Task results (or errors) are logged as a result string"""
    journal = Journal.objects.get(pk=journal_pk)
    responses = []
    for author in journal.authors.all():
        responses.append(update_author_grade_to_LMS(author.pk, journal))
    return responses
