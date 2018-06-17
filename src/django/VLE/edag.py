from .models import *


def get_sorted_nodes(journal):
    return journal.node_set.annotate(
        sort_deadline=Case(
            When(type != Node.ENTRY, then=('preset__deadline__datetime')),
            default='entry__datetime')
    ).order_by('sort_deadline')
