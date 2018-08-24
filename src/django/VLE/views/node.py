"""
node.py.

In this file are all the node api requests.
"""
from datetime import datetime

from rest_framework import viewsets
from django.db.models import Case, When

import VLE.views.responses as response
import VLE.permissions as permissions

from VLE.serializers import NodeSerializer
from VLE.serializers import JournalSerializer
from VLE.models import Journal, Node
import VLE.edag as edag


class NodeView(viewsets.ModelViewSet):
    """Node view.

    This class creates the following api paths:
    GET /nodes/ -- gets all the nodes
    POST /nodes/ -- create a new node
    GET /nodes/<pk> -- gets a specific node
    PATCH /nodes/<pk> -- partially update a node
    DEL /nodes/<pk> -- delete a node
    """

    serializer_class = NodeSerializer

    def list(self, request):
        """Get all nodes contained within a journal.

        Arguments:
        request -- request data
            jID -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the node data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            journal_id = request.query_params['jID']
        except KeyError:
            return response.keyerror('jID')

        try:
            journal = Journal.objects.get(pk=journal_id)
        except Journal.DoesNotExist:
            return response.not_found('Journal')

        if journal.user is not request.user and \
            not permissions.has_assignment_permission(request.user, journal.assignment,
                                                      'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view journals of other participants.')

        can_add = journal.user == request.user
        can_add = can_add and \
            permissions.has_assignment_permission(request.user, journal.assignment, 'can_edit_journal')

        nodes = journal.node_set.annotate(
            sort_deadline=Case(
                When(type=Node.ENTRY, then='entry__createdate'),
                default='preset__deadline')
        ).order_by('sort_deadline')
        node_dict = []
        added_add_node = False
        for node in nodes:
            if node.type == Node.PROGRESS:
                is_future = (node.preset.deadline - datetime.now()).total_seconds() > 0
                if can_add and not added_add_node and is_future:
                    add_node = JournalSerializer(journal).data
                    if add_node is not None:
                        node_dict.append(add_node)
                    added_add_node = True
            node_dict.append(self.serializer_class(node).data)
        return response.success(node_dict)

    def retrieve(request, jID):
        """Retrieve an assignment.

        Arguments:
        request -- request data
            lti -- if this is set, the pk is an lti_id, not a 'normal' id
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            forbidden -- not allowed to retrieve assignments in this course

        On success:
            succes -- with the assignment data

        """
        """Get all nodes contained within a journal.

        Arguments:
        request -- the request that was sent
        jID     -- the journal id

        Returns a json string containing all entry and deadline nodes.
        """
        user = request.user
        if not user.is_authenticated:
            return response.unauthorized()

        try:
            journal = Journal.objects.get(pk=jID)
        except Journal.DoesNotExist:
            return response.not_found('Journal')

        if not (journal.user is user or permissions.has_assignment_permission(user,
                journal.assignment, 'can_view_assignment_participants')):
            return response.forbidden('You are not allowed to view journals of other participants.')

        return response.success(payload={'nodes': edag.get_nodes_dict(journal, request.user)})
