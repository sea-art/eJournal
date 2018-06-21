from VLE.models import *
import random
import datetime
import django.utils.timezone as timezone


def make_user(username, password, email=None, lti_id=None, profile_picture=None, is_admin=False):
    user = User(username=username, email=email, lti_id=lti_id, is_admin=is_admin)
    user.save()
    user.set_password(password)
    if profile_picture:
        user.profile_picture = profile_picture
    else:
        user.profile_picture = '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_role(name):
    role = Role(name=name)
    role.save()
    return role


def make_participation(user, course, role):
    participation = Participation(user=user, course=course, role=role)
    participation.save()
    return participation


def make_course(name, abbrev, startdate=None, author=None, lti_id=None):
    course = Course(name=name, abbreviation=abbrev, startdate=startdate, author=author, lti_id=lti_id)
    course.save()
    if author:
        participation = Participation()
        participation.user = author
        participation.course = course
        participation.role = Role.objects.get(name='Teacher')
        participation.save()
    return course


def make_assignment(name, description, author=None, format=None, cIDs=None, courses=None):
    """Makes a new assignment

    Arguments:
    name -- name of assignment
    description -- description of the assignment
    author -- author of assignment
    format -- format of assignment
    courseIDs -- ID of the courses the assignment belongs to
    courses -- courses it belongs to

    On success, returns a new assignment.
    """
    if format is None:
        format = JournalFormat()
        format.save()
    assign = Assignment(name=name, description=description, author=author, format=format)
    assign.save()
    if cIDs:
        for cID in cIDs:
            assign.courses.add(Course.objects.get(pk=cID))
    if courses:
        for course in courses:
            assign.courses.add(course)
    return assign


def make_format(templates=[], max_points=10):
    format = JournalFormat(max_points=max_points)
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


def make_entry(template, posttime=timezone.now()):
    """
    Creates a new entry in a journal.
    Posts it at the specified moment, or when unset, now.
    -journal is the journal to post the entry in.
    -posttime is the time of posting, defaults to current time.
    """
    # TODO: Too late logic.

    entry = Entry(template=template, createdate=posttime)
    entry.save()
    return entry


def make_entry_template(name):
    entry_template = EntryTemplate(name=name)
    entry_template.save()
    return entry_template


def make_field(template, descrip, loc, type=Field.TEXT):
    field = Field(type=type, title=descrip, location=loc, template=template)
    field.save()
    return field


def make_content(entry, data, field=None):
    content = Content(field=field, entry=entry, data=data)
    content.save()
    return content


def make_deadline(datetime=datetime.datetime.now(), points=None):
    if points:
        deadline = Deadline(datetime=datetime, points=points)
    else:
        deadline = Deadline(datetime=datetime)
    deadline.save()
    return deadline


def make_journal_format():
    journal_format = JournalFormat()
    journal_format.save()
    return journal_format
