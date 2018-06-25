"""
factory.py.

The facory has all kinds of functions to create entries in the database.
Sometimes this also supports extra functionallity like adding courses to assignments.
"""
from VLE.models import User, Participation, Course, Assignment, Role, JournalFormat, PresetNode, Node, EntryComment, \
    Entry, EntryTemplate, Field, Content, Deadline, Journal
import random
import datetime
import django.utils.timezone as timezone


def make_user(username, password, email=None, lti_id=None, profile_picture=None, is_admin=False):
    """Create a user.

    Arguments:
    username -- username (is the user came from the UvA canvas, this will be its studentID)
    password -- password of the user to login
    email -- mail of the user (default: none)
    lti_id -- to link the user to canvas (default: none)
    profile_picture -- profile picture of the user (default: none)
    is_admin -- if the user needs all permissions, set this true (default: False)
    """
    user = User(username=username, email=email, lti_id=lti_id, is_admin=is_admin)
    user.save()
    user.set_password(password)
    if profile_picture:
        user.profile_picture = profile_picture
    else:
        user.profile_picture = '/static/oh_no/{}.png'.format(random.randint(1, 10))
    user.save()
    return user


def make_participation(user=None, course=None, role=None):
    """Create a participation.

    Arguments:
    user -- user that participates
    course -- course the user participates in
    role -- role the user has on the course
    """
    participation = Participation(user=user, course=course, role=role)
    participation.save()
    return participation


def make_course(name, abbrev, startdate=None, author=None, lti_id=None):
    """Create a course.

    Arguments:
    name -- name of the course
    abbrev -- abbreviation of the course
    startdate -- startdate of the course
    author -- author of the course, this will also get the teacher role as participation
    lti_id -- potential lti_id, this is to link the canvas course to the VLE course.
    """
    course = Course(name=name, abbreviation=abbrev, startdate=startdate, author=author, lti_id=lti_id)
    course.save()
    if author:
        role = factory.make_role_all_permissions("Teacher", course)
        make_participation(author, course, role)
    return course


def make_assignment(name, description, author=None, format=None, cIDs=None, courses=None):
    """Make a new assignment.

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
    """Make a format.

    Arguments:
    templates -- list of all the templates to add to the format.
    max-points -- maximum points of the format (default: 10)

    Returns the format
    """
    format = JournalFormat(max_points=max_points)
    format.save()
    format.available_templates.add(*templates)
    return format


def make_progress_node(format, deadline):
    """Make a progress node.

    Arguments:
    format -- format the node belongs to.
    deadline -- deadline of the node.
    """
    node = PresetNode(type=Node.PROGRESS, deadline=deadline, format=format)
    node.save()
    return node


def make_entrydeadline_node(format, deadline, template):
    """Make entry deadline.

    Arguments:
    format -- format of the entry deadline.
    deadline -- deadline en the entry deadline.
    template -- template of the entrydeadline.
    """
    node = PresetNode(type=Node.ENTRYDEADLINE, deadline=deadline,
                      forced_template=template, format=format)
    node.save()
    return node


def make_node(journal, entry):
    """Make a node.

    Arguments:
    journal -- journal the node belongs to.
    entry -- entry the node belongs to.
    """
    node = Node(type=Node.ENTRY, entry=entry, journal=journal)
    node.save()
    return node


def make_journal(assignment, user):
    """Make a new journal.

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
    """Create a new entry in a journal.

    Posts it at the specified moment, or when unset, now.
    Arguments:
    journal -- is the journal to post the entry in.
    posttime -- is the time of posting (defaults: now).
    """
    # TODO: Too late logic.

    entry = Entry(template=template, createdate=posttime)
    entry.save()
    return entry


def make_entry_template(name):
    """Make an entry template."""
    entry_template = EntryTemplate(name=name)
    entry_template.save()
    return entry_template


def make_field(template, descrip, loc, type=Field.TEXT):
    """Make a field."""
    field = Field(type=type, title=descrip, location=loc, template=template)
    field.save()
    return field


def make_content(entry, data, field=None):
    """Make content."""
    content = Content(field=field, entry=entry, data=data)
    content.save()
    return content


def make_deadline(datetime=datetime.datetime.now(), points=None):
    """Make deadline (with possible points).

    Arguments:
    datetime -- time the deadline ends (default: now)
    points -- points that have to be aquired to pass the deadline.
    """
    if points:
        deadline = Deadline(datetime=datetime, points=points)
    else:
        deadline = Deadline(datetime=datetime)
    deadline.save()
    return deadline


def make_journal_format():
    """Make a journal format."""
    journal_format = JournalFormat()
    journal_format.save()
    return journal_format


def make_role(name, course, can_edit_course_roles=False, can_view_course_participants=False,
              can_edit_course=False, can_delete_course=False,
              can_add_assignment=False, can_view_assignment_participants=False,
              can_delete_assignment=False, can_publish_assigment_grades=False,
              can_grade_journal=False, can_publish_journal_grades=False,
              can_edit_journal=False, can_comment_journal=False):
    """Make a role using the given permissions.

    A complete overview of the role requirements can be found here:
    https://docs.google.com/spreadsheets/d/1M7KnEKL3cG9PMWfQi9HIpRJ5xUMou4Y2plnRgke--Tk

    Arguments:
    name -- name of the role (needs to be unique)
    can_... -- permission
    """
    role = Role(
        name=name,
        course=course,

        can_edit_course_roles=can_edit_course_roles,
        can_view_course_participants=can_view_course_participants,
        can_edit_course=can_edit_course,
        can_delete_course=can_delete_course,

        can_add_assignment=can_add_assignment,
        can_view_assignment_participants=can_view_assignment_participants,
        can_delete_assignment=can_delete_assignment,
        can_publish_assigment_grades=can_publish_assigment_grades,

        can_grade_journal=can_grade_journal,
        can_publish_journal_grades=can_publish_journal_grades,
        can_edit_journal=can_edit_journal,
        can_comment_journal=can_comment_journal
    )
    role.save()
    return role


def make_role_all_permissions(name):
    """Make a role with all permissions enabled.

    This enables a participant of the course to do everything within that course.
    This should not be confused with the global roles: these also have effect
    outside of the course."""
    make_role(name, True, True, True, True, True, True,
              True, True, True, True, True, True)


def make_entrycomment(entry, author, text):
    """Make an Entry Comment.

    Make an Entry Comment for an entry based on its ID.
    With the author and the given text.
    Arguments:
    entry -- entry where the comment belongs to
    author -- author of the comment
    text -- content of the comment
    """
    return EntryComment.objects.create(
        entry=entry,
        author=author,
        text=text
    )
