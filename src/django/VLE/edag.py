"""
edag.py.

Useful edag functions.
"""
from django.db.models import Case, When
from django.utils import timezone
from VLE.models import Node
import VLE.serializers as serialize
import VLE.permissions as permissions


def get_sorted_nodes(journal):
    """Get sorted nodes.

    Get all the nodes of a journal in sorted order.
    Order is default by deadline.
    """
    return journal.node_set.annotate(
        sort_deadline=Case(
            When(type=Node.ENTRY, then='entry__createdate'),
            default='preset__deadline')
    ).order_by('sort_deadline')


def get_nodes_dict(journal, user):
    """Convert a journal to a list of node dictionaries.

    First sorts the nodes on date, then attempts to add an
    add-node if the user can add to the journal, the subsequent
    progress node is in the future and maximally one.
    """
    can_add = journal.user == user
    can_add = can_add and permissions.has_assignment_permission(user, journal.assignment, 'can_edit_journal')

    nodes = get_sorted_nodes(journal)
    node_dict = []
    added_add_node = False
    for node in nodes:
        if node.type == Node.PROGRESS:
            is_future = (node.preset.deadline - timezone.now()).total_seconds() > 0
            if can_add and not added_add_node and is_future:
                add_node = serialize.add_node_dict(journal)
                if add_node is not None:
                    node_dict.append(add_node)
                added_add_node = True
        node_dict.append(serialize.node_to_dict(node, user))
    return node_dict
