"""
node.py.

In this file are all the node api requests.
"""
from rest_framework import viewsets
from datetime import datetime

import VLE.views.responses as response
import VLE.permissions as permissions

from VLE.models import Journal
import VLE.timeline as timeline


class NodeView(viewsets.ModelViewSet):
    """Node view.

    This class creates the following api paths:
    GET /nodes/ -- gets all the nodes

    TODO:
    POST /nodes/ -- create a new node
    GET /nodes/<pk> -- gets a specific node
    PATCH /nodes/<pk> -- partially update a node
    DEL /nodes/<pk> -- delete a node
    """

    def list(self, request):
        """Get all nodes contained within a journal.

        Arguments:
        request -- request data
            journal_id -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the node data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            journal_id = request.query_params['journal_id']
        except KeyError:
            return response.keyerror('journal_id')

        journal = Journal.objects.get(pk=journal_id)

        if journal.user != request.user and \
            not permissions.has_assignment_permission(request.user, journal.assignment,
                                                      'can_view_assignment_journals'):
            return response.forbidden('You are not allowed to view journals of other participants.')

        if ((journal.assignment.unlock_date and journal.assignment.unlock_date > datetime.now()) or
            (journal.assignment.lock_date and journal.assignment.lock_date < datetime.now())) and \
           not permissions.has_assignment_permission(request.user, journal.assignment,
                                                     'can_view_assignment_journals'):
            return response.bad_request('The assignment is locked and unavailable for students.')

        return response.success({'nodes': timeline.get_nodes(journal, request.user)})
