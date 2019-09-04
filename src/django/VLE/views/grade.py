"""
grade.py.

In this file are all the grade api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
from VLE.models import Comment, Entry, Grade
from VLE.serializers import EntrySerializer, GradeHistorySerializer


class GradeView(viewsets.ViewSet):
    """Grade view.

    This class creates the following api paths:
    GET /grades/ -- gets the grade history of an entry
    POST /grades/ -- grade an entry
    """

    def list(self, request):
        """Get the grade history of an entry.

        Arguments:
        request -- request data
            entry_id -- entry ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when its not their own journal, or the user is not allowed to grade that journal
        On success:
            success -- with all historic grades corresponding to the entry
        """
        entry_id, = utils.required_typed_params(request.query_params, (int, "entry_id"))

        entry = Entry.objects.get(pk=entry_id)
        assignment = entry.node.journal.assignment

        request.user.check_permission('can_view_grade_history', assignment)

        grade_history = Grade.objects.filter(entry=entry)

        return response.success({'grade_history': GradeHistorySerializer(grade_history, many=True).data})

    def create(self, request):
        """Set a new grade for an entry.

        Arguments:
        request -- request data
            entry_id -- entry ID
            grade -- grade
            published -- published state

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            key_error -- missing keys
            not_found -- could not find the entry, author or assignment

        On success:
            success -- with the assignment data
        """
        entry_id, grade, published = utils.required_typed_params(request.data, (int, 'entry_id'), (float, 'grade'),
                                                                 (bool, 'published'))

        entry = Entry.objects.get(pk=entry_id)
        journal = entry.node.journal
        assignment = journal.assignment

        request.user.check_permission('can_grade', assignment)

        if published:
            request.user.check_permission('can_publish_grades', assignment)

        if grade is not None and grade < 0:
            return response.bad_request('Grade must be greater than or equal to zero.')

        grade = factory.make_grade(entry, request.user.pk, grade, published)

        if published:
            Comment.objects.filter(entry=entry).update(published=True)

        return response.created({
            'entry': EntrySerializer(entry, context={'user': request.user}).data,
            'lti': lti_grade.replace_result(journal)
        })
