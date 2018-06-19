from rest_framework.decorators import api_view
from django.http import JsonResponse

from VLE.serializers import *
import VLE.factory as factory


@api_view(['POST'])
def create_new_course(request):
    """Create a new course

    Arguments:
    request -- the request that was send with
    name -- name of the course
    abbr -- abbreviation of the course
    startdate -- date when the course starts

    Returns a json string for if it is succesful or not.
    """
    course = factory.make_course(request.data["name"], request.data["abbr"], request.data["startdate"], request.user)

    return JsonResponse({'result': 'success', 'course': course_to_dict(course)})


@api_view(['POST'])
def create_new_assignment(request):
    """Create a new course

    Arguments:
    request -- the request that was send with
    name -- name of the course
    abbr -- abbreviation of the course
    startdate -- date when the course starts

    Returns a json string for if it is succesful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = make_course(request.data['name'], request.data['description'], request.user)

    return JsonResponse({'result': 'success', 'course': course_to_dict(course)}, status=200)


@api_view(['POST'])
def create_journal(request, aID):
    """ Create a new journal

    Arguments:
    request -- the request that was send with
    aID -- the assignment id
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    assignment = Assignment.objects.get(pk=aID)
    journal = make_journal(assignment, request.user)

    return JsonResponse({'result': 'success', 'journal': journal_to_dict(journal)}, status=200)


@api_view(['POST'])
def create_entry(request):
    """ Create a new entry
    TODO: How to match new Entry (Deadline) with a pre-existing Node?
    Arguments:
    request -- the request that was send with
    jID -- the journal id
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        jID = request.data['jID']
        journal = Journal.objects.get(pk=jID, user=request.user)

        tID = request.data['tID']
        template = EntryTemplate.objects.get(pk=request.data['tID'])

        # TODO: content.

        # TODO: Check if node can still be created (deadline passed? graded?)
        if 'nID' in request.data:
            nID = request.data['nID']
            node = Node.objects.get(pk=nID, journal=journal)
            if node.type == Node.PROGRESS:
                return JsonResponse({'result': '400 Bad Request'}, status=400)

            node.entry = make_entry(template)

        else:
            entry = make_entry(template)
            node = make_node(journal, entry)

        return JsonResponse({'result': 'success', 'node': node_to_dict(node)}, status=200)
    except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
        return JsonResponse({'result': '400 Bad Request'}, status=400)
