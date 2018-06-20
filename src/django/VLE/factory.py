from VLE.models import *
import random
import datetime
import django.utils.timezone as timezone


def hex_to_dec(hex):
    """Change hex string to int"""
    return int(hex, 16)


def dec_to_hex(dec):
    """Change int to hex value"""
    return hex(dec).split('x')[-1]


def check_permissions(user, cID, permissionList):
    """Check whether the user has the right permissions to access the given
    course functionality.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    role = get_role(user, cID)

    for permission in permissionList:
        if not getattr(role, permission):
            return False

    return True


def get_role(user, cID):
    """Get the role (with permissions) of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    role = Role.objects.get(id=roleID)

    return role


def get_permissions(user, cID):
    """Get the permissions of the given user in the given course.

    Arguments:
    user -- user that did the request.
    cID -- course ID used to validate the request.
    """
    assert not(user is None or cID is None)
    # First get the role ID of the user participation.
    roleID = Participation.objects.get(user=user, course=cID).id
    # Now get the role and its corresponding permissions.
    role = Role.objects.get(id=roleID)

    return vars(role)


def is_admin(user):
    """Check whether the user is an administrator.

    Arguments:
    user -- user that did the request.
    """
    assert not(user is None)

    is_admin = User.objects.get(user=user).is_admin

    return is_admin


def make_user(username, password, email=None, lti_id=None, profile_picture=None):
    user = User(username=username, email=email, lti_id=lti_id)
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


def make_course(name, abbrev, startdate=None, author=None):
    course = Course(name=name, abbreviation=abbrev, startdate=startdate, author=author)
    course.save()
    if author:
        participation = Participation()
        participation.user = author
        participation.course = course
        participation.role = Role.objects.get(name='Teacher')
        participation.save()
    return course


def make_assignment(name, description, courseID=None, author=None, format=None, deadline=None):
    if format is None:
        format = JournalFormat()
        format.save()
    assign = Assignment(name=name, description=description, author=author, deadline=deadline, format=format)
    assign.save()
    if courseID:
        assign.courses.add(Course.objects.get(pk=courseID))
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
