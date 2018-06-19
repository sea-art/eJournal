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

    course = factory.make_assignment(
        request.data['name'],
        request.data['description'],
        request.data['courseID'],
        request.user
    )

    return JsonResponse({'result': 'success', 'assignment': assignment_to_dict(course)})


@api_view(['GET'])
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
def create_entry(request, jID):
    """ Create a new entry
    TODO: How to match new Entry (Deadline) with a pre-existing Node?
    Arguments:
    request -- the request that was send with
    jID -- the journal id
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    journal = Journal.objects.get(pk=jID)

    return JsonResponse({'result': 'success', 'journal': journal_to_dict(journal)})
