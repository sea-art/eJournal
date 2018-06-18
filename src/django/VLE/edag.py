from django.db.models import Case, When
from .models import *


def get_sorted_nodes(journal):
    return journal.node_set.annotate(
        sort_deadline=Case(
            When(type=Node.ENTRY, then='entry__datetime'),
            default='preset__deadline__datetime')
    ).order_by('sort_deadline')


def node_to_dict(node):
    if node.type == Node.ENTRY:
        return entry_node_to_dict(node)
    elif node.type == Node.ENTRYDEADLINE:
        return entry_deadline_to_dict(node)
    elif node.type == Node.PROGRESS:
        return progress_to_dict(node)
    return None

def entry_node_to_dict(node):
    return {
        'type': node.type,
        'journal': node.journal.id,
        'entry': entry_to_str(node.entry),
    }

def entry_to_dict(entry):
    return {
        'template': template_to_dict(entry.template),
        
    }