from rest_framework import serializers
from VLE.models import *
from random import randint
import VLE.utils as utils


def user_to_dict(user):
    return {
        'name': user.username,
        'picture': user.profile_picture,
        'uID': user.id
    } if user else None


def participation_to_dict(participation):
    role_dict = {'role': participation.role.name}
    user_dict = user_to_dict(participation.user)

    return {**role_dict, **user_dict} if participation else None


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
        'description': assignment.description,
        'auth': user_to_dict(assignment.author),
    } if assignment else None


def journal_to_dict(journal):
    entries = utils.get_journal_entries(journal)
    return {
        'jID': journal.id,
        'student': user_to_dict(journal.user),
        'stats': {
            'acquired_points': utils.get_acquired_grade(entries, journal),
            'graded': utils.get_graded_count(entries),
            'submitted': utils.get_submitted_count(entries),
            'total_points': utils.get_max_points(journal),
        }
    } if journal else None


def add_node_dict(journal):
    return {
        'type': 'a',
        'nID': -1,
        'templates': [template_to_dict(template) for template in journal.assignment.format.available_templates.all()]
    } if journal else None


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
        'jID': node.id,
        'entry': entry_to_dict(node.entry),
    } if node else None


def entry_deadline_to_dict(node):
    return {
        'type': node.type,
        'nID': node.id,
        'jID': node.id,
        'deadline': node.preset.deadline.datetime.strftime('%d-%m-%Y %H:%M'),
        'entry': entry_to_dict(node.entry),
    } if node else None


def progress_to_dict(node):
    return {
        'type': node.type,
        'nID': node.id,
        'jID': node.id,
        'deadline': node.preset.deadline.datetime.strftime('%d-%m-%Y %H:%M'),
        'target': node.preset.deadline.points,
    } if node else None


def entry_to_dict(entry):
    return {
        'eID': entry.id,
        'createdate': entry.createdate.strftime('%Y-%m-%d %H:%M'),
        'grade': entry.grade,
        # 'late': TODO
        'template': template_to_dict(entry.template),
        'content': [content_to_dict(content) for content in entry.content_set.all()],
    } if entry else None


def template_to_dict(template):
    return {
        'tID': template.id,
        'name': template.name,
        'fields': [field_to_dict(field) for field in template.field_set.all()],
    } if template else None


def field_to_dict(field):
    return {
        'tag': field.id,
        'type': field.type,
        'title': field.title,
        'location': field.location,
    } if field else None


def content_to_dict(content):
    return {
        'tag': content.field.pk,
        'data': content.data,
    } if content else None


def format_to_dict(format):
    return {
        'fID': format.id,
        'templates': [template_to_dict(template) for template in format.available_templates.all()],
        'presets': [preset_to_dict(preset) for preset in format.presetnode_set.all()],
    } if format else None


def preset_to_dict(preset):
    if not preset:
        return None

    base = {
        'type': preset.type,
        'deadline': preset.deadline.datetime.strftime('%Y-%m-%d %H:%M'),
    }

    if preset.type == Node.PROGRESS:
        result = {**base, **{'target': preset.deadline.points}}
    elif preset.type == Node.ENTRYDEADLINE:
        result = {**base, **{'template': template_to_dict(preset.forced_template)}}

    return result
