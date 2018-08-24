"""
extra.py.

In this file are all the extra api requests.
This includes:
    /names/ -- to get the names belonging to the ids
"""
from rest_framework.decorators import api_view
import VLE.views.responses as response
from VLE.models import Course, Journal, Assignment, EntryTemplate
import VLE.permissions as permissions
import VLE.utils.generic_utils as utils


@api_view(['GET'])
def names(request, cID, aID, jID):
    """Get names of course, assignment, journal.

    Arguments:
    request -- the request that was sent
        cID -- optionally the course id
        aID -- optionally the assignment id
        jID -- optionally the journal id

    Returns a json string containing the names of the set fields.
    cID populates 'course', aID populates 'assignment', tID populates
    'template' and jID populates 'journal' with the users' name.
    """
    if not request.user.is_authenticated:
        return response.unauthorized()

    cID, aID, jID = utils.optional_params(request.data, "cID", "aID", "jID")
    result = {}

    try:
        if cID:
            course = Course.objects.get(pk=cID)
            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not allowed to view this course.')
            result['course'] = course.name
        if aID:
            assignment = Assignment.objects.get(pk=aID)
            if not (assignment.courses.all() & request.user.participations.all()):
                return response.forbidden('You are not allowed to view this assignment.')
            result['assignment'] = assignment.name
        if jID:
            journal = Journal.objects.get(pk=jID)
            if not (journal.user == request.user or permissions.has_assignment_permission(request.user,
                    journal.assignment, 'can_view_assignment_participants')):
                return response.forbidden('You are not allowed to view journals of other participants.')
            result['journal'] = journal.user.first_name + " " + journal.user.last_name

    except (Course.DoesNotExist, Assignment.DoesNotExist, Journal.DoesNotExist, EntryTemplate.DoesNotExist):
        return response.not_found('Course, Assignment, Journal or Template does not exist.')

    return response.success(result)
