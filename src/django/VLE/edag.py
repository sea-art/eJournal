from django.db.models import Case, When
from .models import *


def get_nodes_dict(journal):
    nodes = get_sorted_nodes(journal)
    node_dict = [node_to_dict(node) for node in nodes]
    return node_dict


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
        'entry': entry_to_dict(node.entry),
    }


def entry_deadline_to_dict(node):
    return {
        'type': node.type,
        'journal': node.journal.id,
        'entry': entry_to_dict(node.entry),
        'deadline': node.preset.deadline.datetime
    }


def progress_to_dict(node):
    return {
        'type': node.type,
        'journal': node.journal.id,
        'deadline': node.preset.deadline.datetime,
        'target': node.preset.deadline.points,
    }


def entry_to_dict(entry):
    if entry is None:
        return {}

    return {
        'eID': entry.id,
        'template': template_to_dict(entry.template),
        'createdate': entry.datetime,
        'grade': entry.grade,
        'late': entry.late,
        'content': [content_to_dict(content) for content in entry.content_set.all()],
    }


def template_to_dict(template):
    return {
        'fields': [field_to_dict(field) for field in template.field_set.all()],
        'name': template.name,
    }


def field_to_dict(field):
    return {
        'tag': template.id,
        'type': template.type,
        'title': template.title,
        'location': template.location,
    }


def content_to_dict(content):
    return {
        'field': content.field.pk,
        'data': content.data,
    }
