from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse
import json

from VLE.serializers import *
import VLE.factory as factory
import VLE.utils as utils


@api_view(['POST'])
def create_new_course(request):
    """Create a new course

    Arguments:
    request -- the request that was send with
        name -- name of the course
        abbr -- abbreviation of the course
        startdate -- optional date when the course starts
        lti_id -- optional lti_id to link the course to

    On success, returns a json string containing the course.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        name, abbr = utils.get_required_post_params(request.data, "name", "abbr")
        startdate, lti_id = utils.get_optional_post_params(request.data, "startdate", "lti_id")
    except KeyError:
        return utils.keyerror_json("name", "abbr")

    course = factory.make_course(name, abbr, startdate, request.user, lti_id)

    return JsonResponse({'result': 'success', 'course': course_to_dict(course)})


@api_view(['POST'])
def create_new_assignment(request):
    """Create a new assignment

    Arguments:
    request -- the request that was send with
        name -- name of the assignment
        description -- description of the assignment
        cID -- id of the course the assignment belongs to

    On success, returns a json string containing the assignment.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        name, description, cID = utils.get_required_post_params(request.data, "name", "description", "cID")
    except KeyError:
        return utils.keyerror_json("name", "description", "cID")

    assignment = factory.make_assignment(name, description, cIDs=[cID], author=request.user)
    return JsonResponse({'result': 'success', 'assignment': assignment_to_dict(assignment)})


@api_view(['POST'])
def create_journal(request):
    """Create a new journal

    Arguments:
    request -- the request that was send with
    aID -- the assignment id
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        aID = utils.get_required_post_params(request.data, "aID")
    except KeyError:
        return utils.keyerror_json("aID")

    assignment = Assignment.objects.get(pk=aID)
    journal = factory.make_journal(assignment, request.user)

    return JsonResponse({'result': 'success', 'journal': journal_to_dict(journal)})


@api_view(['POST'])
@parser_classes([JSONParser])
def create_entry(request):
    """ Create a new entry
    Arguments:
    request -- the request that was send with
    jID -- the journal id
    tID -- the template id to create the entry with
    nID -- optional: the node to bind the entry to (only for entrydeadlines)
    content -- the list of {tag, data} tuples to bind data to a template field.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        jID, tID, content_list = utils.get_required_post_params(request.data, "jID", "tID", "content")
        nID, = utils.get_optional_post_params(request.data, "nID")
    except KeyError:
        return utils.keyerror_json("jID", "tID", "content")

    try:
        journal = Journal.objects.get(pk=jID, user=request.user)

        template = EntryTemplate.objects.get(pk=tID)

        # TODO: Check if node can still be created (deadline passed? graded?)
        if nID:
            node = Node.objects.get(pk=nID, journal=journal)
            if node.type == Node.PROGRESS:
                return JsonResponse({'result': '400 Bad Request',
                                     'description': 'Passed node is a Progress node.'},
                                    status=400)

            node.entry = factory.make_entry(template)

        else:
            entry = factory.make_entry(template)
            node = factory.make_node(journal, entry)

        for content in content_list:
            data = content['data']
            tag = content['tag']
            field = Field.objects.get(pk=tag)
            factory.make_content(node.entry, data, field)

        return JsonResponse({'result': 'success', 'nodes': edag.get_nodes_dict(journal)}, status=200)
    except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Journal, Template or Node does not exist.'},
                            status=404)


@api_view(['POST'])
def create_entrycomment(request):
    """Create a new entrycomment
    Arguments:
    request -- the request that was send with
        entryID -- the entry id
        authorID -- the author id
        text -- the comment
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        entryID, authorID, text = utils.get_required_post_params(request.data, "entryID", "authorID", "text")
    except KeyError:
        return utils.keyerror_json("entryID", "authorID", "text")

    author = User.objects.get(pk=authorID)
    comment = make_entrycomment(entryID, author, text)

    return JsonResponse({'result': 'success'})
