"""
journal.py.

In this file are all the journal api requests.
"""
from rest_framework import viewsets
from VLE.serializers import JournalSerializer
from VLE.models import Journal, Assignment
import VLE.permissions as permissions
import VLE.views.responses as response
import VLE.utils.generic_utils as utils
import VLE.lti_grade_passback as lti_grade


class JournalView(viewsets.ViewSet):
    """Journal view.

    This class creates the following api paths:
    GET /journals/ -- gets all the journals
    GET /journals/<pk> -- gets a specific journal
    POST /journals/ -- create a new journal
    PATCH /journals/<pk> -- partially update an journal
    DEL /journals/<pk> -- delete an journal
    """

    def list(self, request):
        """Get the student submitted journals of one assignment.

        Arguments:
        request -- request data
            assignment_id -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exist
            forbidden -- when the user has no permission to view the journals of the assignment
        On succes:
            success -- with journals and stats about the journals

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        assignment = Assignment.objects.get(pk=request.query_params['assignment_id'])

        if not permissions.has_assignment_permission(request.user, assignment, 'can_view_assignment_journals'):
            return response.forbidden('You are not allowed to view assignment participants.')

        queryset = assignment.journal_set.all()
        journals = JournalSerializer(queryset, many=True).data

        return response.success({'journals': journals})

    def retrieve(self, request, pk):
        """Get a student submitted journal.

        Arguments:
        request -- request data
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exist
            forbidden -- when the user has no permission to view the journal
        On succes:
            success -- with journals and stats about the journals

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        journal = Journal.objects.get(pk=pk)

        if not (journal.user == request.user and
                permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal')) and \
           not permissions.has_assignment_permission(request.user, journal.assignment, 'can_view_assignment_journals'):
            return response.forbidden('You are not allowed to view this journal.')

        serializer = JournalSerializer(journal)

        return response.success({'journal': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing journal.

        Arguments:
        request -- request data
            data -- the new data for the journal
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exist
            forbidden -- User not allowed to edit this journal
            unauthorized -- when the user is unauthorized to edit the journal
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new journal data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk = kwargs.get('pk')

        journal = Journal.objects.get(pk=pk)

        published, = utils.optional_params(request.data, 'published')
        if published:
            return self.publish(request, journal)

        if not request.user.is_superuser:
            return response.forbidden('You are not allowed to edit this journal.')

        req_data = request.data
        del req_data['published']
        serializer = JournalSerializer(journal, data=req_data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()

        return response.success({'journal': serializer.data})

    def publish(self, request, journal, published=True):
        if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_publish_grades'):
            return response.forbidden('You cannot publish assignments.')

        utils.publish_all_journal_grades(journal, published)
        if journal.sourcedid is not None and journal.grade_url is not None:
            payload = lti_grade.replace_result(journal)
        else:
            payload = None

        return response.success({'lti_info': payload})
