import django.utils.timezone as timezone

from VLE.models import User
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import JournalFormat
from VLE.models import PresetNode
from VLE.models import Node
from VLE.models import Entry
from VLE.models import Content


def make_user(username, password):
    user = User(username=username)
    user.save()
    user.set_password(password)
    user.save()
    return user


def make_course(name, abbrev):
    course = Course(name=name, abbreviation=abbrev)
    course.save()
    return course


def make_assignment(name, description, author, format=None):
    if format is None:
        format = JournalFormat()
        format.save()
    assign = Assignment(name=name, description=description, author=author, format=format)
    assign.save()
    return assign


def make_format(templates=[]):
    format = JournalFormat()
    format.save()
    format.available_templates.add(*templates)
    return format


def make_progress_node(format, deadline):
    node = PresetNode(type=Node.PROGRESS, deadline=deadline, format=format)
    node.save()
    return node


def make_entrydeadline_node(format, deadline, template):
    node = PresetNode(type=Node.ENTRYDEADLINE, deadline=deadline,
                      forced_template=template, format=format)
    node.save()
    return node


def make_node(journal, entry):
    node = Node(type=Node.ENTRY, entry=entry, journal=journal)
    node.save()
    return node


def make_journal(assignment, user):
    """
    Creates a new journal.
    First creates all nodes defined by the format.
    The deadlines and templates are the same object
    as those in the format, so any changes should
    be reflected in the Nodes as well.
    """
    preset_nodes = assignment.format.presetnode_set.all()
    journal = Journal(assignment=assignment, user=user)
    journal.save()

    for preset_node in preset_nodes:
        Node(type=preset_node.type,
             journal=journal,
             preset=preset_node).save()

    return journal


def make_entry(template, content, posttime=timezone.now()):
    """
    Creates a new entry in a journal.
    Posts it at the specified moment, or when unset, now.
    -journal is the journal to post the entry in.
    -content is a list of tuples (tag, data) to attach to the entry.
    -posttime is the time of posting, defaults to current time.
    """
    # TODO: Too late logic.
    if posttime:
        entry = Entry(template=template, datetime=posttime, late=False)
    entry.save()

    for tag, data in content:
        field = Content(entry=entry, tag=tag, data=data)
        field.save()
    return entry
