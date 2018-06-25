"""
update.py.

API functions that handle the update requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

import VLE.serializers as serialize
import VLE.utils as utils
import VLE.factory as factory
from VLE.models import Course, EntryComment, Assignment, Participation, Role, Entry, Journal, EntryTemplate, Node


@api_view(['POST'])
def update_course(request):
    """Update an existing course.

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
    return JsonResponse({'result': 'success', 'course': serialize.course_to_dict(course)}, status=200)


@api_view(['POST'])
def update_assignment(request):
    """Update an existing assignment.

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

    return JsonResponse({'result': 'success', 'assignment': serialize.assignment_to_dict(assignment)},
                        status=200)


@api_view(['POST'])
def update_password(request):
    """Update a password.

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


@api_view(['POST'])
def update_grade_notification(request):
    """Update whether the user gets notified when a grade changes/new grade.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        user.grade_notifications = request.data['new_value']
    except Exception:
        return JsonResponse({'result': '400 Bad Request'}, status=400)

    user.save()
    return JsonResponse({'result': 'success', 'new_value': user.grade_notifications})


@api_view(['POST'])
def update_comment_notification(request):
    """Update whether the user gets notified when a comment changes/new comment.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        user.comment_notifications = request.data['new_value']
    except Exception:
        return JsonResponse({'result': '400 Bad Request'}, status=400)

    user.save()
    return JsonResponse({'result': 'success', 'new_value': user.comment_notifications})


@api_view(['POST'])
@parser_classes([JSONParser])
def update_format(request):
    """ Update a format
    Arguments:
    request -- the request that was send with
    aID -- the assignments' format to update
    templates -- the list of templates to bind to the format
    presets -- the list of presets to bind to the format
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        aID, templates, presets, unused_templates = utils.get_required_post_params(request.data,
                                                                                   "aID",
                                                                                   "templates",
                                                                                   "presets",
                                                                                   "unused_templates")
    except KeyError:
        return utils.keyerror_json("fID", "templates", "presets", "unused_templates")

    try:
        assignment = Assignment.objects.get(pk=aID)
        format = assignment.format
    except Assignment.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Format does not exist.'},
                            status=404)

    format.available_templates.all().delete()
    format.unused_templates.all().delete()

    for template_field in templates:
        tID = template_field['tID']
        try:
            format.available_templates.add(EntryTemplate.objects.get(pk=tID))
        except EntryTemplate.DoesNotExist:
            return JsonResponse({'result': '404 Not Found',
                                 'description': 'Template does not exist.'},
                                status=404)

    for template_field in unused_templates:
        tID = template_field['tID']
        try:
            format.unused_templates.add(EntryTemplate.objects.get(pk=tID))
        except EntryTemplate.DoesNotExist:
            return JsonResponse({'result': '404 Not Found',
                                 'description': 'Template does not exist.'},
                                status=404)

    format.presetnode_set.all().delete()

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
            except EntryTemplate.DoesNotExist:
                return JsonResponse({'result': '404 Not Found',
                                     'description': 'Template does not exist.'},
                                    status=404)
            deadline = factory.make_deadline(date)
            factory.make_entrydeadline_node(format, deadline, template)

    return JsonResponse({'result': 'success', 'node': serialize.format_to_dict(format)}, status=200)


@api_view(['POST'])
def update_user_role_course(request):
    """Update user role in a course.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    try:
        uID, cID = utils.get_required_post_params(request.data, "uID", "cID")
    except KeyError:
        return utils.keyerror_json("uID", "cID")

    try:
        participation = Participation.objects.get(user=request.data['uID'], course=request.data['cID'])
        participation.role = Role.objects.get(name=request.data['role'])
    except (Participation.DoesNotExist, Role.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Participation or Role does not exist.'}, status=404)

    participation.save()
    return JsonResponse({'result': 'success', 'new_role': participation.role.name}, status=200)


@api_view(['POST'])
def update_grade_entry(request, eID):
    """Update the entry grade.

    Arguments:
    request -- the request that was send with
    grade -- the grade
    published -- published
    eID -- the entry id

    Returns a json string if it was sucessful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    entry = Entry.objects.get(pk=eID)
    entry.grade = request.data['grade']
    entry.published = request.data['published']
    entry.save()
    return JsonResponse({'result': 'success', 'new_grade': entry.grade, 'new_published': entry.published})


@api_view(['POST'])
def update_publish_grade_entry(request, eID):
    """Update the grade publish status for one entry.

    Arguments:
    request -- the request that was send with
    eID -- the entry id

    Returns a json string if it was sucessful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    publish = request.data['published']
    entry = Entry.objects.get(pk=eID)
    entry.published = publish
    entry.save()
    return JsonResponse({'result': 'success', 'new_published': entry.published})


@api_view(['POST'])
def update_publish_grades_assignment(request, aID):
    """Update the grade publish status for whole assignment.

    Arguments:
    request -- the request that was send with
    aID -- assignment ID

    Returns a json string if it was sucessful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    assign = Assignment.objects.get(pk=aID)
    utils.publish_all_assignment_grades(assign, request.data['published'])
    return JsonResponse({'result': 'success', 'new_published': request.data['published']})


@api_view(['POST'])
def update_publish_grades_journal(request, jID):
    """Update the grade publish status for a journal.

    Arguments:
    request -- the request that was send with
    jID -- journal ID

    Returns a json string if it was sucessful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    journ = Journal.objects.get(pk=jID)
    utils.publish_all_journal_grades(journ, request.data['published'])
    return JsonResponse({'result': 'success', 'new_published': request.data['published']})


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
        entrycommentID, text = utils.get_required_post_params(request.data, "entrycommentID", "text")
    except KeyError:
        return utils.keyerror_json("entrycommentID")

    try:
        comment = EntryComment.objects.get(pk=entrycommentID)
    except EntryComment.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Entrycomment does not exist.'},
                            status=404)
    comment.text = text
    comment.save()
    return JsonResponse({'result': 'success'})


@api_view(['POST'])
def update_user_data(request):
    """Update user data.

    Arguments:
    request -- the update request that was send with
        username -- new password of the user
        picture -- current password of the user

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    if 'username' in request.data:
        user.username = request.data['username']
    if 'picture' in request.data:
        user.profile_picture = request.data['picture']

    user.save()
    return JsonResponse({'result': 'success', 'user': serialize.user_to_dict(user)}, status=200)


@api_view(['POST'])
@parser_classes([JSONParser])
def update_template(request):
    """ Update a template
    Arguments:
    request -- the request that was send with
    tID -- optionally the template to update
    fields -- the list of fields of the new template
    name -- the (new) name of the template
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    tID, = utils.get_optional_post_params(request.data, "tID")
    try:
        fields, name = utils.get_required_post_params(request.data, "fields", "name")
    except KeyError:
        return utils.keyerror_json("fields", "name")

    try:
        if tID:
            template = EntryTemplate.objects.get(pk=tID)
            template.name = name
        else:
            template = factory.make_entry_template(name)
    except EntryTemplate.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Template does not exist.'},
                            status=404)

    template.field_set.all().delete()

    for field in fields:
        type = field['type']
        title = field['title']
        location = field['location']

        factory.make_field(template, title, location, type)

    template.save()
    return JsonResponse({'result': 'success', 'template': serialize.template_to_dict(template)}, status=200)
