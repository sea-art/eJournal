"""
update.py.

API functions that handle the update requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from django.http import JsonResponse

import VLE.views.responses as responses
import VLE.serializers as serialize
import VLE.utils as utils
import VLE.factory as factory
from VLE.models import Course, EntryComment, Assignment, Participation, Role, Entry, \
    User, Journal, EntryTemplate, Node, PresetNode

import re


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
    course.abbreviation = request.data['abbr']
    course.startdate = request.data['startDate']
    course.save()
    return JsonResponse({'result': 'success', 'course': serialize.course_to_dict(course)}, status=200)


@api_view(['POST'])
def update_course_with_studentID(request):
    """Update an existing course with a student.

    Arguments:
    request -- the update request that was send with
        uID -- student ID given with the request
        cID -- course ID given with the request

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        user = User.objects.get(pk=request.data['uID'])
        course = Course.objects.get(pk=request.data['cID'])

    except (User.DoesNotExist, Course.DoesNotExist, Participation.DoesNotExist):
        return JsonResponse({'result': '404 Not Found',
                             'description': 'User, Course or Participation does not exist.'}, status=404)

    #  TODO use roles from course
    role = Role.objects.get(name="Student")
    participation = factory.make_participation(user, course, role)

    participation.save()
    return JsonResponse({'result': 'Succesfully added student to course'}, status=200)


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
        return JsonResponse({'result': '401 Authentication Error', 'description': 'Wrong password'}, status=401)

    password = request.data['new_password']
    if len(password) < 8:
        return JsonResponse({
            'result': '400 Bad request',
            'description': 'Password needs to contain at least 8 characters'
        }, status=400)
    if password == password.lower():
        return JsonResponse({
            'result': '400 Bad request',
            'description': 'Password needs to contain at least 1 capital letter'
        }, status=400)
    if re.match(r'^\w+$', password):
        return JsonResponse({
            'result': '400 Bad request',
            'description': 'Password needs to contain a special character'
        }, status=400)

    user.set_password(password)
    user.save()
    return JsonResponse({'result': 'success', 'description': 'Succesfully changed the password'}, status=200)


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
    return JsonResponse({'result': 'success', 'new_value': user.grade_notifications}, status=200)


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
    return JsonResponse({'result': 'success', 'new_value': user.comment_notifications}, status=200)


def update_templates(result_list, templates):
    """ Create new templates for those which have changed,
    and removes the old one.

    Entries have to keep their original template, so that the content
    does not change after a template update, therefore when a template
    is updated, the template is recreated from scratch and bound to
    all nodes that use the previous template, if there were any.
    """
    for template_field in templates:
        if 'updated' in template_field and template_field['updated']:
            # Create the new template and add it to the format.
            new_template = parse_template(template_field)
            result_list.add(new_template)

            # Update presets to use the new template.
            if 'tID' in template_field and template_field['tID'] > 0:
                template = EntryTemplate.objects.get(pk=template_field['tID'])
                presets = PresetNode.objects.filter(forced_template=template).all()
                for preset in presets:
                    preset.forced_template = new_template
                    preset.save()

                result_list.remove(template)


def parse_template(template_dict):
    """ Parse a new template according to the passed JSON-serialized template. """
    name = template_dict['name']
    fields = template_dict['fields']

    template = factory.make_entry_template(name)

    for field in fields:
        type = field['type']
        title = field['title']
        location = field['location']

        factory.make_field(template, title, location, type)

    template.save()
    return template


def swap_templates(from_list, goal_list, target_list):
    """ Swap templates from from_list to target_list if they are present in goal_list. """
    for template in goal_list:
        if from_list.filter(pk=template['tID']).count() > 0:
            template = from_list.get(pk=template['tID'])
            from_list.remove(template)
            target_list.add(template)


def update_journals(journals, preset, created):
    """ Create or update the preset node in all relevant journals.

    Arguments:
    journals -- the journals to update.
    preset -- the preset node to update the journals with.
    created -- whether the preset node was newly created.
    """
    if created:
        for journal in journals:
            factory.make_node(journal, None, preset.type, preset)
    else:
        for journal in journals:
            journal.node_set.filter(preset=preset).update(type=preset.type)


def update_presets(assignment, presets):
    """ Update preset nodes in the assignment according to the passed list.

    Arguments:
    assignment -- the assignment to update the presets in.
    presets -- a list of JSON-serialized presets.
    """
    format = assignment.format
    for preset in presets:
        exists = 'pID' in preset

        if exists:
            try:
                preset_node = PresetNode.objects.get(pk=preset['pID'])
            except EntryTemplate.DoesNotExist:
                return JsonResponse({'result': '404 Not Found',
                                     'description': 'Preset does not exist.'},
                                    status=404)
        else:
            preset_node = PresetNode(format=format)

        type_changed = preset_node.type != preset['type']
        preset_node.type = preset['type']
        preset_node.deadline = preset['deadline']

        if preset_node.type == Node.PROGRESS:
            preset_node.target = preset['target']
        elif preset_node.type == Node.ENTRYDEADLINE:
            template_field = preset['template']

            if 'tID' in template_field and template_field['tID'] > 0:
                preset_node.forced_template = EntryTemplate.objects.get(pk=template_field['tID'])
            else:
                preset_node.forced_template = parse_template(template_field)

        preset_node.save()
        if type_changed:
            update_journals(assignment.journal_set.all(), preset_node, not exists)


def delete_presets(presets, remove_presets):
    """ Deletes all presets in remove_presets from presets. """
    pIDs = []
    for preset in remove_presets:
        pIDs.append(preset['pID'])

    presets.filter(pID__in=pIDs).delete()


def delete_templates(templates, remove_templates):
    """ Deletes all templates in remove_templates from templates. """
    tIDs = []
    for template in remove_templates:
        tIDs.append(template['tID'])

    templates.filter(tID__in=tIDs).delete()


@api_view(['POST'])
@parser_classes([JSONParser])
def update_format(request):
    """ Update a format
    Arguments:
    request -- the request that was send with
        aID -- the assignments' format to update
        templates -- the list of templates to bind to the format
        presets -- the list of presets to bind to the format
        unused_templates -- the list of templates that are bound to the template
                            deck, but are not used in presets nor the entry templates.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    try:
        aID, templates, presets = utils.required_params(request.data, "aID", "templates", "presets")
        unused_templates = utils.required_params(request.data, "unused_templates")
        removed_presets, removed_templates = utils.required_params(request.data, "removed_presets", "removed_templates")
    except KeyError:
        return responses.keyerror("aID", "templates", "presets", "unused_templates")

    try:
        assignment = Assignment.objects.get(pk=aID)
        format = assignment.format
    except Assignment.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Format does not exist.'},
                            status=404)

    update_presets(assignment, presets)
    update_templates(format.available_templates, templates)
    update_templates(format.unused_templates, unused_templates)

    # Swap templates from lists if they occur in the other:
    # If a template was previously unused, but is now used, swap it to available templates, and vice versa.
    swap_templates(format.available_templates, unused_templates, format.unused_templates)
    swap_templates(format.unused_templates, templates, format.available_templates)

    delete_presets(format.presets, removed_presets)
    delete_templates(format.available_templates, removed_templates)
    delete_templates(format.unused_templates, removed_templates)

    return JsonResponse({'result': 'success', 'format': serialize.format_to_dict(format)}, status=200)


@api_view(['POST'])
def update_user_role_course(request):
    """Update user role in a course.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is succesful or not.
    """
    try:
        uID, cID = utils.required_params(request.data, "uID", "cID")
    except KeyError:
        return responses.keyerror("uID", "cID")

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
    return JsonResponse({'result': 'success', 'new_grade': entry.grade, 'new_published': entry.published}, status=200)


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
    return JsonResponse({'result': 'success', 'new_published': entry.published}, status=200)


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
    return JsonResponse({'result': 'success', 'new_published': request.data['published']}, status=200)


@api_view(['POST'])
def update_publish_grades_journal(request, jID):
    """Update the grade publish status for a journal.

    Arguments:
    request -- the request that was send with
        published -- publish state of grade
    jID -- journal ID

    Returns a json string if it was sucessful or not.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'result': '401 Authentication Error'}, status=401)

    journ = Journal.objects.get(pk=jID)
    utils.publish_all_journal_grades(journ, request.data['published'])
    return JsonResponse({'result': 'success', 'new_published': request.data['published']}, status=200)


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
        entrycommentID, text = utils.required_params(request.data, "entrycommentID", "text")
    except KeyError:
        return responses.keyerror("entrycommentID")

    try:
        comment = EntryComment.objects.get(pk=entrycommentID)
    except EntryComment.DoesNotExist:
        return JsonResponse({'result': '404 Not Found',
                             'description': 'Entrycomment does not exist.'},
                            status=404)
    comment.text = text
    comment.save()
    return JsonResponse({'result': 'success'}, status=200)


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
