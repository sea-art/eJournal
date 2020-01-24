from __future__ import absolute_import, unicode_literals

from celery import shared_task
from django.conf import settings

from VLE.models import AssignmentParticipation, Entry, Journal, Node
from VLE.utils import grading


@shared_task
def left_journal_passback(author_pk, journal_pk):
    journal = Journal.objects.get(pk=journal_pk)
    author = AssignmentParticipation.objects.get(pk=author_pk)
    return grading.send_author_status_to_LMS(journal, author, left_journal=True)


@shared_task
def join_journal_passback(author_pk, journal_pk):
    journal = Journal.objects.get(pk=journal_pk)
    author = AssignmentParticipation.objects.get(pk=author_pk)
    return grading.send_author_status_to_LMS(journal, author)
