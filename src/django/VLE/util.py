from VLE.models import *
import random
import datetime
import django.utils.timezone as timezone


def make_user(username, password, email=None, lti_id=None, profile_picture=None):
    user = User(username=username, email=email, lti_id=lti_id)
    user.save()
    user.set_password(password)
    user.profile_picture = profile_picture if profile_picture else '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_course(name, abbrev, date=None):
    course = Course(name=name, abbreviation=abbrev, startdate=date)
    course.save()
    return course


def make_assignment(name, description, author=None, format=None):
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


def make_entry_template(name):
    entry_template = EntryTemplate(name=name)
    entry_template.save()
    return entry_template


def make_field(descrip, loc, template, type='t'):
    field = Field(type=type, description=descrip, location=loc, template=template)
    field.save()
    return field


def make_content(entry, data, field=None):
    content = Content(field=field, entry=entry, data=data)
    content.save()
    return content


def make_deadline(format, datetime=datetime.datetime.now()):
    deadline = Deadline(format=format, datetime=datetime)
    deadline.save()
    return deadline


def make_journal_format():
    journal_format = JournalFormat()
    journal_format.save()
    return journal_format
