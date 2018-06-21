from rest_framework.decorators import api_view
from django.http import JsonResponse

from VLE.serializers import *
import VLE.factory as factory
import VLE.utils as utils
from VLE.views.get import get_own_user_data


@api_view(['POST'])
def update_course(request):
    """Updates an existing course.

    Arguments:
    request -- the update request that was send with
        name -- name of the course
        abbr -- abbreviation of the course
        startdate -- date when the course starts

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    course = Course.objects.get(pk=request.data['cID'])
    course.name = request.data['name']
    course.abbr = request.data['abbr']
    course.startdate = request.data['startDate']
    course.save()
    return JsonResponse({'result': 'success', 'course': course_to_dict(course)})


@api_view(['POST'])
def update_assignment(request):
    """Updates an existing assignment.

    Arguments:
    request -- the update request that was send with
        name -- name of the assignment
        description -- description of the assignment
        deadline -- deadline of the assignment

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    assignment = Assignment.objects.get(pk=request.data['aID'])
    assignment.name = request.data['name']
    assignment.description = request.data['description']
    assignment.save()

    return JsonResponse({'result': 'success', 'assignment': assignment_to_dict(assignment)})


@api_view(['POST'])
def update_password(request):
    """Updates a password.

    Arguments:
    request -- the update request that was send with
        new_password -- new password of the user
        old_password -- current password of the user

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated or not user.check_password(request.data['old_password']):
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    # TODO: Add some real password validations
    if len(request.data['new_password']) <= 3:
        return JsonResponse({'result': '400 Bad request'}, status=400)

    user.set_password(request.data['new_password'])
    user.save()
    return JsonResponse({'result': 'success'})


@api_view(['GET'])
def update_grade_notification(request, notified):
    """Updates whether the user gets notified when a grade changes/new grade.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    if notified == 'true':
        user.grade_notifications = True
    elif notified == 'false':
        user.grade_notifications = False
    else:
        return JsonResponse({'result': '400 Bad Request'}, status=400)

    user.save()
    return JsonResponse({'result': 'success', 'new_value': user.grade_notifications})


@api_view(['GET'])
def update_comment_notification(request, notified):
    """Updates whether the user gets notified when a comment changes/new comment.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    if notified == 'true':
        user.comment_notifications = True
    elif notified == 'false':
        user.comment_notifications = False
    else:
        return JsonResponse({'result': '400 Bad Request'}, status=400)

    user.save()
    return JsonResponse({'result': 'success', 'new_value': user.comment_notifications})


@api_view(['POST'])
def update_entrycomment(request):
    """
    Update a comment to an entry.

    Arguments:
    request -- the request that was send with
        entrycommentID -- The ID of the entrycomment.
        text -- The updated text.
    Returns a json string for if it is succesful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        comment = EntryComment.objects.get(pk=request['entrycommentID'])
        comment.text = request['text']
        comment.save()
        return JsonResponse({'result': 'success'})
    except:
        return JsonResponse({'result': '500 Internal Server Error'}, status=500)


@api_view(['POST'])
def update_user_data(request):
    """Updates user data.

    Arguments:
    request -- the update request that was send with
        username -- new password of the user
        picture -- current password of the user

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    print(request.data)
    if 'username' in request.data:
        user.username = request.data['username']
    if 'picture' in request.data:
        user.profile_picture = request.data['picture']

    user.save()
    return JsonResponse({'result': 'success', 'user': user_to_dict(user)})
