"""
course.py.

In this file are all the course api requests.
"""
from rest_framework import viewsets

from VLE.serializers import JournalSerializer
from VLE.models import Journal, Assignment
import VLE.permissions as permissions
import VLE.views.responses as response
import VLE.utils.generic_utils as utils
import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade
from rest_framework.decorators import action


class JournalView(viewsets.ViewSet):
    """Journal view.

    This class creates the following api paths:
    GET /journals/ -- gets all the journals
    POST /journals/ -- create a new journal
    GET /journals/<pk> -- gets a specific journal
    PATCH /journals/<pk> -- partially update an journal
    DEL /journals/<pk> -- delete an journal
    PATCH /journals/published_state/<pk> -- update the published state of all entries in a journal
    """

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
        """Create a new assignment.

        Arguments:
        request -- request data
            aID -- assignment ID

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
            [aID] = utils.required_params(request.data, "aID")
        except KeyError:
            return response.keyerror("aID")

        role = permissions.get_assignment_id_permissions(request.user, aID)
        if not role:
            return response.forbidden("You have no permissions within this course.")
        elif not role["can_edit_journal"]:
            return response.forbidden("You have no permissions to create a journal.")

        assignment = Assignment.objects.get(pk=aID)
        journal = factory.make_journal(assignment, request.user)
        serializer = self.serializer_class(journal, many=False)
        return response.created({'journal': serializer.data})

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

        return response.success({'journal': self.serializer_class(journal).data})

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        pass

    def destroy(self, request, *args, **kwargs):
        pass

    @action(methods=['patch'], detail=True)
    def published_state(self, request, *args, **kwargs):
        """Update the grade publish status for a journal.

        Arguments:
        request -- the request that was send with
            published -- publish state of grade
            jID -- journal ID

        Returns a json string if it was successful or not.
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        jID = kwargs.get('pk')
        published = utils.required_params(request.data, 'published')

        try:
            journ = Journal.objects.get(pk=jID)
        except Journal.DoesNotExist:
            return response.DoesNotExist('Journal')

        if not permissions.has_assignment_permission(request.user, journ.assignment, 'can_publish_journal_grades'):
            return response.forbidden('You cannot publish assignments.')

        utils.publish_all_journal_grades(journ, published)

        if journ.sourcedid is not None and journ.grade_url is not None:
            payload = lti_grade.replace_result(journ)
        else:
            payload = dict()

        payload['new_published'] = request.data['published']
        return response.success(payload=payload)
