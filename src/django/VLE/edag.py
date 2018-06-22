from django.db.models import Case, When
from django.utils import timezone
from .models import *
import VLE.serializers as serializers


def get_sorted_nodes(journal):
    return journal.node_set.annotate(
        sort_deadline=Case(
            When(type=Node.ENTRY, then='entry__createdate'),
            default='preset__deadline__datetime')
    ).order_by('sort_deadline')


def get_nodes_dict(journal):
    nodes = get_sorted_nodes(journal)
    node_dict = []
    added_add_node = False
    for node in nodes:
        if node.type == Node.PROGRESS:
            if (not added_add_node and (node.preset.deadline.datetime - timezone.now()).total_seconds() > 0):
                node_dict.append(serializers.add_node_dict(journal))
                added_add_node = True
        node_dict.append(serializers.node_to_dict(node))
    return node_dict
