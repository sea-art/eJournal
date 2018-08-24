"""
create.py.

API functions that handle the create requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from django.utils.timezone import now

import VLE.serializers as serialize
import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.utils.email_handling as email_handling
from VLE.models import User, Journal, EntryTemplate, Node, Assignment, Field, Entry, Content, Course
import VLE.edag as edag
import VLE.lti_grade_passback as lti_grade
import VLE.validators as validators

import VLE.views.responses as responses
import VLE.permissions as permissions

import jwt
import json
from django.conf import settings

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
        eID -- the entry id
        uID -- the author id
        text -- the comment
        published -- the comment's publishment state
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        eID, uID, text, published = utils.required_params(request.data, "eID", "uID", "text", "published")
    except KeyError:
        return responses.keyerror("eID", "uID", "text", "published")

    try:
        author = User.objects.get(pk=uID)
        entry = Entry.objects.get(pk=eID)
        assignment = Assignment.objects.get(journal__node__entry=entry)
    except (User.DoesNotExist, Entry.DoesNotExist):
        return responses.not_found('User or Entry does not exist.')

    if not (author == user):
        return responses.forbidden('You are not allowed to write comments for others.')

    published = published or not permissions.has_assignment_permission(user, assignment, 'can_grade_journal')

    entrycomment = factory.make_entrycomment(entry, author, text, published)
    return responses.created(payload={'comment': serialize.entrycomment_to_dict(entrycomment)})
