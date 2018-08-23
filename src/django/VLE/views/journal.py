"""
course.py.

In this file are all the course api requests.
"""
import statistics as st

from rest_framework import viewsets

import VLE.views.responses as response
from VLE.serializers import JournalSerializer
from VLE.models import Journal, Assignment
import VLE.permissions as permissions


class JournalView(viewsets.ViewSet):
    serializer_class = JournalSerializer

    def list(self, request):
        """Get the student submitted journals of one assignment.

        Arguments:
        request -- request data
            aID -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when aID is not set
            not found -- when the assignment does not exists
            forbidden -- when the user has no permission to view the journals of the assignment
        On succes:
            success -- with journals and stats about the journals
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            assignment = Assignment.objects.get(pk=request.query_params['aID'])
        except KeyError:
            return response.keyerror('aID')
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        if not permissions.has_assignment_permission(request.user, assignment, 'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view assignment participants.')

        journals = []

        queryset = assignment.journal_set.all()
        journals = self.serializer_class(queryset, many=True).data

        stats = {}
        if journals:
            # TODO: Maybe make this efficient for minimal delay?
            # TODO: Add real stats
            stats['needsMarking'] = 5  # sum([x['stats']['submitted'] - x['stats']['graded'] for x in journals])
            # points = [x['stats']['acquired_points'] for x in journals]
            stats['avgPoints'] = 2  # round(st.mean(points), 2)

        return response.success({
            'stats': stats if stats else None,
            'journals': journals
        })

    def create(self, request):
        pass

    def retrieve(self, request, pk):
        """Get a student submitted journal.

        Arguments:
        request -- request data
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exists
            forbidden -- when the user has no permission to view the journal
        On succes:
            success -- with journals and stats about the journals
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            journal = Journal.objects.get(pk=pk)
        except Journal.DoesNotExist:
            return response.not_found('Journal')

        if journal.user is not request.user and \
           not permissions.has_assignment_permission(request.user, journal.assignment,
                                                     'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view this journal.')

        return response.success(self.serializer_class(journal).data)

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass
