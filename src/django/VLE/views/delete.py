"""
delete.py.

API functions that handle the delete requests.
"""
from rest_framework.decorators import api_view

from VLE.models import Assignment, Course, EntryComment, Participation, User, Role

import VLE.views.responses as responses
import VLE.utils.generic_utils as utils
import VLE.permissions as permissions


@api_view(['POST'])
def delete_entrycomment(request):
    """Delete an entrycomment.

    Arguments:
    request -- the request that was send with
        ecID -- the entrycomment ID
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        ecID = utils.required_params(request.data, "ecID")[0]
    except KeyError:
        return responses.keyerror("ecID")

    try:
        entrycomment = EntryComment.objects.get(pk=ecID)
        entryAuthor = User.objects.get(pk=entrycomment.author.id)
    except (EntryComment.DoesNotExist, User.DoesNotExist):
        return responses.not_found('Comment or Author does not exist.')

    if not user == entryAuthor:
        return responses.forbidden()

    EntryComment.objects.get(id=ecID).delete()
    return responses.success(description='Succesfully deleted comment.')
