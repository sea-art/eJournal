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


class NodeView(viewsets.ModelViewSet):
    serializer_class = NodeSerializer

    def list(self, request):
        """Get all nodes contained within a journal.

        Arguments:
        request -- request data
            jID -- journal ID

        Returns a json string containing all entry and deadline nodes.
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
