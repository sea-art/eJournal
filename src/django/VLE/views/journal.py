"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets

from VLE.serializers import JournalSerializer
from VLE.models import Journal, Assignment, Course
import VLE.permissions as permissions
import VLE.views.responses as response
import VLE.utils.generic_utils as utils
import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade


class JournalView(viewsets.ViewSet):
    """Journal view.

    This class creates the following api paths:
    GET /journals/ -- gets all the journals
    GET /journals/<pk> -- gets a specific journal
    POST /journals/ -- create a new journal
    PATCH /journals/<pk> -- partially update an journal

    TODO:
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
            keyerror -- when assignment_id is not set
            not found -- when the assignment does not exist
            forbidden -- when the user has no permission to view the journals of the assignment
        On succes:
            success -- with journals and stats about the journals

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            assignment = Assignment.objects.get(pk=request.query_params['assignment_id'])
        except KeyError:
            return response.keyerror('assignment_id')
        except Assignment.DoesNotExist:
            return response.not_found('Assignment does not exist.')

        if not permissions.has_assignment_permission(request.user, assignment, 'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view assignment participants.')

        journals = []

        queryset = assignment.journal_set.all()
        journals = JournalSerializer(queryset, many=True).data

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

        try:
            journal = Journal.objects.get(pk=pk)
        except Journal.DoesNotExist:
            return response.not_found('Journal does not exist.')

        if journal.user != request.user and \
           not permissions.has_assignment_permission(request.user, journal.assignment,
                                                     'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view this journal.')

        serializer = JournalSerializer(journal)

        return response.success({'journal': serializer.data})

    def create(self, request):
        """Create a new journal.

        Arguments:
        request -- request data
            assignment_id -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            key_error -- missing keys
            forbidden -- the user is not allowed to create assignments in this course

        On success:
            succes -- with the journal data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            assignment_id, = utils.required_params(request.data, "assignment_id")
        except KeyError:
            return response.keyerror("assignment_id")

        role = permissions.get_assignment_id_permissions(request.user, assignment_id)
        if not role:
            return response.forbidden("You have no permissions within this course.")
        elif not role["can_edit_journal"]:
            return response.forbidden("You have no permissions to create a journal.")

        try:
            assignment = Assignment.objects.get(pk=assignment_id)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment does not exist.')

        journal = factory.make_journal(assignment, request.user)
        serializer = JournalSerializer(journal, many=False)
        return response.created({'journal': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing journal.

        Arguments:
        request -- request data
            data -- the new data for the course
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

        try:
            journal = Journal.objects.get(pk=pk)
        except Journal.DoesNotExist:
            return response.not_found('Journal does not exist.')

        published, = utils.optional_params(request.data, 'published')
        if published:
            return self.publish(request, journal)
        if permissions.has_assignment_permission(request.user, journal.assignment, 'can_edit_journal'):
            req_data = request.data
            del req_data['published']
            # TODO Check if a serializer is valid if we add an extra argument (published) to the request data.
            serializer = JournalSerializer(journal, data=req_data, partial=True)
            if not serializer.is_valid():
                response.bad_request()
            serializer.save()
        else:
            return response.forbidden('You are not allowed to edit this journal.')

        return response.success({'journal': serializer.data})

    def publish(self, request, journal, published=True):
        if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_publish_journal_grades'):
            return response.forbidden('You cannot publish assignments.')

        utils.publish_all_journal_grades(journal, published)
        if journal.sourcedid is not None and journal.grade_url is not None:
            payload = lti_grade.replace_result(journal)
        else:
            payload = None

        return response.success({'lti_info': payload})
