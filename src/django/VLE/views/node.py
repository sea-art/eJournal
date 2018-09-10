"""
node.py.

In this file are all the node api requests.
"""
from rest_framework import viewsets

import VLE.views.responses as response
import VLE.permissions as permissions

from VLE.models import Journal
import VLE.edag as edag


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

        try:
            journal = Journal.objects.get(pk=journal_id)
        except Journal.DoesNotExist:
            return response.not_found('Journal does not exist.')

        if journal.user != request.user and \
            not permissions.has_assignment_permission(request.user, journal.assignment,
                                                      'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view journals of other participants.')

        can_add = journal.user == request.user
        can_add = can_add and \
            permissions.has_assignment_permission(request.user, journal.assignment, 'can_edit_journal')

        return response.success({'nodes': edag.get_nodes(journal, request.user)})
