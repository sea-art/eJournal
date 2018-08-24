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
from VLE.models import User, Journal, EntryTemplate, Node, Assignment, Field, Entry, Content, Course
import VLE.edag as edag
import VLE.lti_grade_passback as lti_grade
import VLE.validators as validators

import VLE.views.responses as responses
import VLE.permissions as permissions


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
