"""
Serializers.

Functions to convert certain data to other formats.
"""
import VLE.utils as utils
from VLE.models import Journal, Node


def user_to_dict(user):
    """Convert user object to dictionary."""
    return {
        'name': user.username,
        'picture': user.profile_picture,
        'uID': user.id
    } if user else None


def participation_to_dict(participation):
    """Convert participation to a dictionary.

    Parameters
    ----------
    participation : Participation
        The participation to convert.

    Returns
    -------
    dictionary
        Dictionary of the role and user dictionaries.

    """
    role_dict = {'role': participation.role.name}
    user_dict = user_to_dict(participation.user)

    return {**role_dict, **user_dict} if participation else None


def course_to_dict(course):
    """Convert course to a dictionary."""
    return {
        'cID': course.id,
        'name': course.name,
        'auth': user_to_dict(course.author),
        'date': course.startdate,
        'abbr': course.abbreviation
    } if course else None


def student_assignment_to_dict(assignment, user):
    """Convert a student assignment to a dictionary."""
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
    """Convert deadline to dictionary."""
    if not assignment:
        return None

    assignment_dict = assignment_to_dict(assignment)
    assignment_dict['courses'] = [course_to_dict(c) for c in assignment.courses.all()]

    return assignment_dict


def assignment_to_dict(assignment):
    """Convert assignment to dictionary."""
    return {
        'aID': assignment.id,
        'name': assignment.name,
        'description': assignment.description,
        'auth': user_to_dict(assignment.author),
    } if assignment else None


def journal_to_dict(journal):
    """Convert a journal to a dictionary."""
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
    """Convert a add_node to a dictionary."""
    return {
        'type': 'a',
        'nID': -1,
        'templates': [template_to_dict(template) for template in journal.assignment.format.available_templates.all()]
    } if journal else None


def node_to_dict(node):
    """Convert a node to a dictionary."""
    if node.type == Node.ENTRY:
        return entry_node_to_dict(node)
    elif node.type == Node.ENTRYDEADLINE:
        return entry_deadline_to_dict(node)
    elif node.type == Node.PROGRESS:
        return progress_to_dict(node)
    return None


def entry_node_to_dict(node):
    """Convert an entrynode to a dictionary."""
    return {
        'type': node.type,
        'nID': node.id,
        'jID': node.id,
        'entry': entry_to_dict(node.entry),
    } if node else None


def entry_deadline_to_dict(node):
    """Convert entrydeadline to a dictionary."""
    return {
        'type': node.type,
        'nID': node.id,
        'jID': node.id,
        'deadline': node.preset.deadline.strftime('%Y-%m-%d %H:%M'),
        'template': template_to_dict(node.preset.forced_template),
        'entry': entry_to_dict(node.entry),
    } if node else None


def progress_to_dict(node):
    """Convert progress node to dictionary."""
    return {
        'type': node.type,
        'nID': node.id,
        'jID': node.id,
        'deadline': node.preset.deadline.strftime('%Y-%m-%d %H:%M'),
        'target': node.preset.target,
    } if node else None


def entry_to_dict(entry):
    """Convert entry to dictionary."""
    return {
        'eID': entry.id,
        'createdate': entry.createdate.strftime('%Y-%m-%d %H:%M'),
        'grade': entry.grade,
        'published': entry.published,
        # 'late': TODO
        'template': template_to_dict(entry.template),
        'content': [content_to_dict(content) for content in entry.content_set.all()],
    } if entry else None


def template_to_dict(template):
    """Convert template to dictionary."""
    return {
        'tID': template.id,
        'name': template.name,
        'fields': [field_to_dict(field) for field in template.field_set.all()],
    } if template else None


def field_to_dict(field):
    """Convert field to dictionary."""
    return {
        'tag': field.id,
        'type': field.type,
        'title': field.title,
        'location': field.location,
    } if field else None


def content_to_dict(content):
    """Convert content to dictionary."""
    return {
        'tag': content.field.pk,
        'data': content.data,
    } if content else None


def format_to_dict(format):
    """Convert format to dictionary."""
    return {
        'unused_templates': [template_to_dict(template) for template in format.unused_templates.all()],
        'templates': [template_to_dict(template) for template in format.available_templates.all()],
        'presets': [preset_to_dict(preset) for preset in format.presetnode_set.all().order_by('deadline')],
    } if format else None


def preset_to_dict(preset):
    """Convert preset node to dictionary."""
    if not preset:
        return None

    base = {
        'pID': preset.id,
        'type': preset.type,
        'deadline': preset.deadline.strftime('%Y-%m-%d %H:%M'),
    }

    if preset.type == Node.PROGRESS:
        result = {**base, **{'target': preset.target}}
    elif preset.type == Node.ENTRYDEADLINE:
        result = {**base, **{'template': template_to_dict(preset.forced_template)}}

    return result


def entrycomment_to_dict(entrycomment):
    """Convert entrycomment to dictionary."""
    return {
        'eID': entrycomment.entry.id,
        'author': user_to_dict(entrycomment.author),
        'text': entrycomment.text,
    } if entrycomment else None
