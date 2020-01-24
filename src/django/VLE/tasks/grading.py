from __future__ import absolute_import, unicode_literals

from celery import shared_task

from VLE import factory
from VLE.models import AssignmentParticipation, Comment, Entry, Journal
from VLE.utils import grading
