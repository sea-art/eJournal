from rest_framework.decorators import api_view, parser_classes, renderer_classes
from rest_framework.parsers import JSONParser
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
    """Create a new assignment

    Arguments:
    request -- the request that was send with
        name -- name of the assignment
        description -- description of the assignment
        courseID -- id of the course the assignment belongs to

    Returns a json string for if it is succesful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    assignment = factory.make_assignment(
        request.data['name'],
        request.data['description'],
        request.data['assignmentID'],
        request.user
    )

    return JsonResponse({'result': 'success', 'assignment': assignment_to_dict(assignment)})


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
    journal = factory.make_journal(assignment, request.user)

    return JsonResponse({'result': 'success', 'journal': journal_to_dict(journal)})


@api_view(['POST'])
@parser_classes((JSONParser,))
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
        jID = request.data['jID']
        journal = Journal.objects.get(pk=jID, user=request.user)

        tID = request.data['tID']
        template = EntryTemplate.objects.get(pk=request.data['tID'])

        content_list = request.data['content']

        # TODO: Check if node can still be created (deadline passed? graded?)
        if 'nID' in request.data:
            print('OOPS')
            nID = request.data['nID']
            node = Node.objects.get(pk=nID, journal=journal)
            if node.type == Node.PROGRESS:
                print('PROGRESS')
                return JsonResponse({'result': '400 Bad Request'}, status=400)

            node.entry = make_entry(template)    

        else:
            entry = make_entry(template)
            node = make_node(journal, entry)

        for content in content_list:
            data = content['data']
            tag = content['tag']
            field = Field.objects.get(pk=tag)
            make_content(node.entry, data, field)

        return JsonResponse({'result': 'success', 'node': node_to_dict(node)}, status=200)
    except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
        print('DOES NOT EXIST')
        return JsonResponse({'result': '400 Bad Request'}, status=400)
