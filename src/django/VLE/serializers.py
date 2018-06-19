from rest_framework import serializers
from VLE.models import *
from random import randint


def user_to_dict(user):
    """Get a object of a single user

    Arguments:
    user -- user to create the object with

    returns dictionary of that user
    """
    return {
        'name': user.username,
        'picture': user.profile_picture,
        'uID': user.id
    } if user else None


def course_to_dict(course):
    return {
        'cID': course.id,
        'name': course.name,
        'auth': user_to_dict(course.author),
        'date': course.startdate,
        'abbr': course.abbreviation
    } if course else None


def student_assignment_to_dict(assignment, user):
    if not assignment:
        return None
    try:
        journal = Journal.objects.get(assignment=assignment, user=user)
    except Journal.DoesNotExist:
        journal = None

    assignment_dict = assignment_to_dict(assignment)
    assignment_dict['journal'] = journal_to_dict(journal) if journal else None

    return assignment_dict


def deadline_to_dict(assignment):
    if not assignment:
        return None

    assignment_dict = assignment_to_dict(assignment)
    assignment_dict['courses'] = [course_to_dict(course) for c in assignment.courses.all()]

    return assignment_dict


def assignment_to_dict(assignment):
    return {
        'aID': assignment.id,
        'name': assignment.name,
        'auth': user_to_dict(assignment.author),
        'description': assignment.description
    } if assignment else None


def journal_to_dict(journal):
    return {
        'jID': journal.id,
        'student': user_to_dict(journal.user),
        'stats': {
            'acquired_points': randint(0, 10),
            'graded': 1,
            'submitted': 1,
            'total_points': 10
        }  # TODO: Change random to real stats
    } if journal else None


def add_node_dict(journal):
    return {
        'type': 'a',
        'nID': -1,
        'templates': [template_to_dict(template) for template in journal.assignment.format.available_templates.all()]
    }


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
        'nID': node.id,
        'entry': entry_to_dict(node.entry),
    }


def entry_deadline_to_dict(node):
    return {
        'type': node.type,
        'nID': node.id,
        'entry': entry_to_dict(node.entry),
        'deadline': node.preset.deadline.datetime.strftime('%d-%m-%Y %H:%M')
    }


def progress_to_dict(node):
    return {
        'type': node.type,
        'nID': node.id,
        'deadline': node.preset.deadline.datetime.strftime('%d-%m-%Y %H:%M'),
        'target': node.preset.deadline.points,
    }


def entry_to_dict(entry):
    if entry is None:
        return {}

    return {
        'eID': entry.id,
        'template': template_to_dict(entry.template),
        'createdate': entry.datetime.strftime('%d-%m-%Y %H:%M'),
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
        'tag': field.id,
        'type': field.type,
        'title': field.title,
        'location': field.location,
    }


def content_to_dict(content):
    return {
        'tag': content.field.pk,
        'data': content.data,
    }
