"""
update.py.

API functions that handle the update requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

import VLE.views.responses as responses
import VLE.serializers as serialize
import VLE.utils as utils
import VLE.permissions as permissions
from VLE.models import Comment, Assignment, Entry, \
    User, Journal
import VLE.lti_grade_passback as lti_grade
from django.conf import settings
import jwt
import json

# Think this one works already
# @api_view(['POST'])
# def connect_assignment_lti(request):
#     """Connect an existing assignment to an lti assignment.
#
#     Arguments:
#     request -- the update request that was send with
#         aID -- the id of the assignment to be linked with lti
#         lti_id -- lti_id that needs to be added to the assignment
#         points_possible -- points_possible in lti assignment
#
#     Returns a json string for if it is succesful or not.
#     """
#     user = request.user
#     if not user.is_authenticated:
#         return responses.unauthorized()
#
#     try:
#         aID, lti_id = utils.required_params(request.data, 'aID', 'lti_id')
#         [points_possible] = utils.optional_params(request.data, 'points_possible')
#     except KeyError:
#         return responses.keyerror('aID')
#
#     try:
#         assignment = Assignment.objects.get(pk=aID)
#     except Assignment.DoesNotExist:
#         return responses.not_found('Assignment')
#
#     if not permissions.has_assignment_permission(user, assignment, 'can_edit_assignment'):
#         return responses.forbidden('You are not allowed to edit the assignment.')
#
#     assignment.lti_id = lti_id
#     if assignment.points_possible is None and points_possible is not '':
#         assignment.points_possible = points_possible
#     assignment.save()
#
#     return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
@parser_classes([JSONParser])
def update_format(request):
    """ Update a format
    Arguments:
    request -- the request that was send with
        aID -- the assignments' format to update
        max_points -- the max points possible.
        templates -- the list of templates to bind to the format
        presets -- the list of presets to bind to the format
        unused_templates -- the list of templates that are bound to the template
                            deck, but are not used in presets nor the entry templates.
        removed_presets -- presets to be removed
        removed_templates -- templates to be removed

    Returns a json string for if it is successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        aID, templates, presets = utils.required_params(request.data, "aID", "templates", "presets")
        unused_templates, max_points = utils.required_params(request.data, "unused_templates", "max_points")
        removed_presets, removed_templates = utils.required_params(request.data, "removed_presets", "removed_templates")

    except KeyError:
        return responses.keyerror("aID", "templates", "presets", "unused_templates", "max_points")

    try:
        assignment = Assignment.objects.get(pk=aID)
        format = assignment.format
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment')

    if not permissions.has_assignment_permission(request.user, assignment, 'can_edit_assignment'):
        return responses.forbidden('You are not allowed to edit this assignment.')

    format.max_points = max_points
    format.save()
    template_map = {}
    utils.update_presets(assignment, presets, template_map)
    utils.update_templates(format.available_templates, templates, template_map)
    utils.update_templates(format.unused_templates, unused_templates, template_map)

    # Swap templates from lists if they occur in the other:
    # If a template was previously unused, but is now used, swap it to available templates, and vice versa.
    utils.swap_templates(format.available_templates, unused_templates, format.unused_templates)
    utils.swap_templates(format.unused_templates, templates, format.available_templates)

    utils.delete_presets(format.presetnode_set, removed_presets)
    utils.delete_templates(format.available_templates, removed_templates)
    utils.delete_templates(format.unused_templates, removed_templates)

    return responses.success(payload={'format': serialize.format_to_dict(format)})


@api_view(['POST'])
def update_grade_entry(request):
    """Update the entry grade.

    Arguments:
    request -- the request that was send with
        grade -- the grade
        published -- published
        eID -- the entry id

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        grade, published, eID = utils.required_params(request.data, 'grade', 'published', 'eID')
    except KeyError:
        return responses.keyerror('grade', 'published', 'eID')

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry')

    journal = entry.node.journal
    if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_grade_journal'):
        return responses.forbidden('You cannot grade or publish entries.')

    entry.grade = grade
    entry.published = published
    entry.save()

    if entry.published and journal.sourcedid is not None and journal.grade_url is not None:
        payload = lti_grade.replace_result(journal)
    else:
        payload = dict()

    payload['new_grade'] = entry.grade
    payload['new_published'] = entry.published

    return responses.success(payload=payload)


@api_view(['POST'])
def update_publish_grade_entry(request):
    """Update the grade publish status for one entry.

    Arguments:
    request -- the request that was send with
        eID -- the entry id

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, eID = utils.required_params(request.data, 'published', 'eID')
    except KeyError:
        return responses.keyerror('published', 'eID')

    try:
        entry = Entry.objects.get(pk=eID)
    except Entry.DoesNotExist:
        return responses.not_found('Entry')

    journal = entry.node.journal
    if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_publish_journal_grades'):
        return responses.forbidden('You cannot publish entries.')

    entry.published = published
    entry.save()

    if published and journal.sourcedid is not None and journal.grade_url is not None:
        payload = lti_grade.replace_result(journal)
    else:
        payload = dict()

    payload['new_published'] = entry.published
    return responses.success(payload={'new_published': entry.published})


@api_view(['POST'])
def update_publish_grades_assignment(request):
    """Update the grade publish status for whole assignment.

    Arguments:
    request -- the request that was send with
        published -- new published state
        aID -- assignment ID

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, aID = utils.required_params(request.data, 'published', 'aID')
    except KeyError:
        return responses.keyerror('aID')

    try:
        assign = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment')

    if not permissions.has_assignment_permission(request.user, assign, 'can_publish_journal_grades'):
        return responses.forbidden('You cannot publish assignments.')

    utils.publish_all_assignment_grades(assign, published)

    for journ in Journal.objects.filter(assignment=assign):
        if journ.sourcedid is not None and journ.grade_url is not None:
            payload = lti_grade.replace_result(journ)
        else:
            payload = dict()

    payload['new_published'] = published
    return responses.success(payload=payload)


@api_view(['POST'])
def update_publish_grades_journal(request):
    """Update the grade publish status for a journal.

    Arguments:
    request -- the request that was send with
        published -- publish state of grade
        jID -- journal ID

    Returns a json string if it was successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        published, jID = utils.required_params(request.data, 'published', 'jID')
    except KeyError:
        return responses.keyerror('published', 'jID')

    try:
        journ = Journal.objects.get(pk=jID)
    except Journal.DoesNotExist:
        return responses.DoesNotExist('Journal')

    if not permissions.has_assignment_permission(request.user, journ.assignment, 'can_publish_journal_grades'):
        return responses.forbidden('You cannot publish assignments.')

    utils.publish_all_journal_grades(journ, published)

    if journ.sourcedid is not None and journ.grade_url is not None:
        payload = lti_grade.replace_result(journ)
    else:
        payload = dict()

    payload['new_published'] = request.data['published']
    return responses.success(payload=payload)


@api_view(['POST'])
def update_entrycomment(request):
    """
    Update a comment to an entry.

    Arguments:
    request -- the request that was send with
        entrycommentID -- The ID of the entrycomment.
        text -- The updated text.
    Returns a json string for if it is successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        entrycommentID, text = utils.required_params(request.data, "entrycommentID", "text")
    except KeyError:
        return responses.keyerror("entrycommentID")

    try:
        comment = Comment.objects.get(pk=entrycommentID)
    except Comment.DoesNotExist:
        return responses.not_found('Entrycomment does not exist.')

    if not permissions.has_assignment_permission(request.user, comment.entry.node.journal.assignment,
                                                 'can_comment_journal'):
        return responses.forbidden('You cannot comment on entries.')

    comment.text = text
    comment.save()
    return responses.success()

# TODO: Test if lti works!
# @api_view(['POST'])
# def update_lti_id_to_user(request):
#     """Create a new user with lti_id.
#
#     Arguments:
#     request -- the request
#         username -- username of the new user
#         password -- password of the new user
#         first_name -- first_name (optinal)
#         last_name -- last_name (optinal)
#         email -- email (optinal)
#         jwt_params -- jwt params to get the lti information from
#             user_id -- id of the user
#             user_image -- user image
#             roles -- role of the user
#     """
#     user = request.user
#     if not user.is_authenticated:
#         return responses.unauthorized()
#
#     if not request.data['jwt_params']:
#         return responses.bad_request()
#
#     lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
#
#     user_id, user_image = lti_params['user_id'], lti_params['user_image']
#     is_teacher = json.load(open('config.json'))['Teacher'] == lti_params['roles']
#     first_name, last_name, email = utils.optional_params(request.data, 'first_name', 'last_name', 'email')
#
#     if first_name is not None:
#         user.first_name = first_name
#     if last_name is not None:
#         user.last_name = last_name
#     if email is not None:
#         if User.objects.filter(email=email).exists():
#             return responses.bad_request('User with this email already exists.')
#
#         user.email = email
#     if user_image is not None:
#         user.profile_picture = user_image
#     if is_teacher:
#         user.is_teacher = is_teacher
#
#     if User.objects.filter(lti_id=user_id).exists():
#         return responses.bad_request('User with this lti id already exists.')
#
#     user.lti_id = user_id
#
#     user.save()
#
#     return responses.success(payload={'user': serialize.user_to_dict(user)})
