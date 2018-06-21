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
    """Updates a password

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
    """Updates whether the user gets notified when a grade changes/new grade

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
    """Updates whether the user gets notified when a comment changes/new comment

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
@parser_classes([JSONParser])
def update_format(request):
    """ Update a format
    Arguments:
    request -- the request that was send with
    fID -- the format to update
    templates -- the list of templates to bind to the format
    presets -- the list of presets to bind to the format
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        fID, templates, presets = utils.get_required_post_params(request.data, "fID", "templates", "presets")
    except KeyError:
        return utils.keyerror_json("fID", "templates", "preset")

    try:
        format = JournalFormat.objects.get(pk=fID)
    except JournalFormat.NotFound:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Format does not exist.'},
                            status=404)

    for template_field in templates:
        tID = template_field['tID']
        try:
            format.available_templates.add(EntryTemplate.objects.get(pk=tID))
        except EntryTemplate.NotFound:
            return JsonResponse({'result': '404 Not Found',
                             'description': 'Template does not exist.'},
                            status=404)
    for preset in presets:
        type = preset['type']
        date = preset['deadline']
        if type == Node.PROGRESS:
            target = preset['target']
            deadline = factory.make_deadline(date, target)
            factory.make_progress_node(format, deadline)

        elif type == Node.ENTRYDEADLINE:
            tID = preset['template']['tID']
            try:
                template = EntryTemplate.objects.get(pk=tID)
            except EntryTemplate.NotFound:
                return JsonResponse({'result': '404 Not Found',
                             'description': 'Template does not exist.'},
                            status=404)
            deadline = factory.make_deadline(date)
            factory.make_entrydeadline_node(format, deadline, template)

        tID = template_field['tID']
        try:
            format.available_templates.add(EntryTemplate.objects.get(pk=tID))
        except EntryTemplate.NotFound:
            return JsonResponse({'result': '404 Not Found',
                             'description': 'Template does not exist.'},
                            status=404)

    return JsonResponse({'result': 'success', 'node': format_to_dict(format)}, status=200)
