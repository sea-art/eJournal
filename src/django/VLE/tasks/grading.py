from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

import VLE.lti_grade_passback as lti_grade
from VLE import factory
from VLE.lti_grade_passback import GradePassBackRequest
from VLE.models import Assignment, AssignmentParticipation, Comment, Entry, Journal
from VLE.utils import grading


@shared_task
def publish_all_assignment_grades(user, assignment_pk):
    """Publish all grades that are not None for an assignment.

    - assignment: the assignment in question
    """
    for journal in Journal.objects.filter(assignment=assignment_pk).distinct():
        publish_all_journal_grades(journal, publisher)
        lti_grade.replace_result(journal)

@shared_task
def publish_all_journal_grades(journal_pk, publisher):
    """publish all grades that are not None for a journal.

    - journal: the journal in question
    - publisher: the publisher of the grade
    """
    entries = Entry.objects.filter(node__journal=journal).exclude(grade=None)

    for entry in entries.filter(grade__published=False):
        factory.make_grade(entry, publisher.pk, entry.grade.grade, True)

    Comment.objects.filter(entry__node__journal=journal).exclude(entry__grade=None).update(published=True)


@shared_task
def update_author_grade_to_LMS(author_pk, journal=None):
    """Sends the grade of an author to the LMS

    It sets the grade to 0 if no journal is found."""
    author = AssignmentParticipation.objects.get(pk=author_pk)
    if journal is None:
        journal = Journal.objects.filter(authors__in=[author]).first()

    return grading.send_grade_to_LMS(journal, author)

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
