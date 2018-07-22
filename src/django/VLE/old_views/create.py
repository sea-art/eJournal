"""
create.py.

API functions that handle the create requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from django.utils.timezone import now

import VLE.serializers as serialize
import VLE.factory as factory
import VLE.utils as utils
from VLE.models import User, Journal, EntryTemplate, Node, Assignment, Field, Entry, Content, Course
import VLE.edag as edag
import VLE.lti_grade_passback as lti_grade

import VLE.views.responses as responses
import VLE.permissions as permissions


@api_view(['POST'])
def create_new_assignment(request):
    """Create a new assignment.

    Arguments:
    request -- the request that was send with
        name -- name of the assignment
        description -- description of the assignment
        cID -- id of the course the assignment belongs to

    On success, returns a json string containing the assignment.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        name, description, cID = utils.required_params(request.data, "name", "description", "cID")
        points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
    except KeyError:
        return responses.keyerror("name", "description", "cID")

    # Assignments can only be created with can_create_assignment permission.
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.unauthorized("You have no access to this course.")
    elif not role.can_add_assignment:
        return responses.forbidden("You have no permissions to create a new assignment.")

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    assignment = factory.make_assignment(name, description, cIDs=[cID],
                                         author=request.user, lti_id=lti_id,
                                         points_possible=points_possible)

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    for user in course.users.all():
        role = permissions.get_role(user, cID)
        if role.can_edit_journal:
            factory.make_journal(assignment, user)

    return responses.created(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
def create_journal(request):
    """Create a new journal.

    Arguments:
    request -- the request that was send with
    aID -- the assignment id

    On success, returns a json string containing the journal.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [aID] = utils.required_params(request.data, "aID")
    except KeyError:
        return responses.keyerror("aID")

    role = permissions.get_assignment_id_permissions(user, aID)

    if role == {}:
        return responses.forbidden("You have no permissions within this course.")
    elif not role["can_edit_journal"]:
        return responses.forbidden("You have no permissions to create a journal.")

    assignment = Assignment.objects.get(pk=aID)
    journal = factory.make_journal(assignment, request.user)

    return responses.created(payload={'journal': serialize.journal_to_dict(journal)})


@api_view(['POST'])
@parser_classes([JSONParser])
def create_entry(request):
    """Create a new entry.

    Arguments:
    request -- the request that was send with
    jID -- the journal id
    tID -- the template id to create the entry with
    nID -- optional: the node to bind the entry to (only for entrydeadlines)
    content -- the list of {tag, data} tuples to bind data to a template field.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        jID, tID, content_list = utils.required_params(request.data, "jID", "tID", "content")
        nID, = utils.optional_params(request.data, "nID")
    except KeyError:
        return responses.keyerror("jID", "tID", "content")

    try:
        journal = Journal.objects.get(pk=jID, user=request.user)

        template = EntryTemplate.objects.get(pk=tID)

        if nID:
            node = Node.objects.get(pk=nID, journal=journal)
            if node.type == Node.PROGRESS:
                return responses.bad_request('Passed node is a Progress node.')

            if node.entry:
                if node.entry.grade is None:
                    if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                        return responses.bad_request('The deadline has already passed.')

                    Content.objects.filter(entry=node.entry).all().delete()
                    node.entry.template = template
                    node.save()
                else:
                    return responses.bad_request('Can not overwrite entry, since it is already graded.')
            else:
                if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                    return responses.bad_request('The deadline has already passed.')

                node.entry = factory.make_entry(template)
                node.save()
        else:
            entry = factory.make_entry(template)
            node = factory.make_node(journal, entry)

        if journal.sourcedid is not None and journal.grade_url is not None:
            lti_grade.needs_grading(journal, node.id)

        for content in content_list:
            data = content['data']
            tag = content['tag']
            field = Field.objects.get(pk=tag)

            factory.make_content(node.entry, data, field)

        result = edag.get_nodes_dict(journal, request.user)
        added = -1
        for i, result_node in enumerate(result):
            if result_node['nID'] == node.id:
                added = i
                break

        return responses.created(payload={'added': added,
                                 'nodes': edag.get_nodes_dict(journal, request.user)})
    except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
        return responses.not_found('Journal, Template or Node does not exist.')


@api_view(['POST'])
def create_entrycomment(request):
    """Create a new entrycomment.

    Arguments:
    request -- the request that was send with
        entryID -- the entry id
        authorID -- the author id
        text -- the comment
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        entryID, authorID, text = utils.required_params(request.data, "entryID", "authorID", "text")
    except KeyError:
        return responses.keyerror("entryID", "authorID", "text")

    try:
        author = User.objects.get(pk=authorID)
        entry = Entry.objects.get(pk=entryID)
    except (User.DoesNotExist, Entry.DoesNotExist):
        return responses.not_found('User or Entry does not exist.')

    entrycomment = factory.make_entrycomment(entry, author, text)
    return responses.created(payload={'comment': serialize.entrycomment_to_dict(entrycomment)})
