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
import VLE.factory as factory
import VLE.validators as validators
from VLE.models import Course, EntryComment, Assignment, Participation, Role, \
    Entry, User, Journal
import VLE.lti_grade_passback as lti_grade
from VLE.settings.base import USER_MAX_FILE_SIZE_MB, USER_MAX_TOTAL_STORAGE_MB
from django.conf import settings
from django.core.exceptions import ValidationError
import re
import jwt
import json


@api_view(['POST'])
def connect_course_lti(request):
    """Connect an existing course to an lti course.

    Arguments:
    request -- the update request that was send with
        lti_id -- lti_id that needs to be added to the course
        cID -- course that needs to be connected to lti_id

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [cID] = utils.required_params(request.data, 'cID')
    except KeyError:
        return responses.keyerror('cID')

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_edit_course:
        return responses.forbidden('You cannot edit this course.')

    course.lti_id = request.data['lti_id']
    course.save()

    return responses.success(payload={'course': serialize.course_to_dict(course)})


@api_view(['POST'])
def update_course(request):
    """Update an existing course.

    Arguments:
    request -- the update request that was send with
        cID -- ID of the course
        name -- name of the course
        abbr -- abbreviation of the course
        startdate -- date when the course starts

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        cID, name, abbr = utils.required_params(request.data, 'cID', 'name', 'abbr')
        startdate, enddate = utils.required_params(request.data, 'startdate', 'enddate')
    except KeyError:
        return responses.keyerror('cID', 'name', 'abbr', 'startdate', 'enddate')

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_edit_course:
        return responses.forbidden('You cannot edit this course.')

    course.name = name
    course.abbreviation = abbr
    course.startdate = startdate
    course.enddate = enddate
    course.save()

    return responses.success(payload={'course': serialize.course_to_dict(course)})


@api_view(['POST'])
def update_course_roles(request):
    """Updates course roles.

    Arguments:
    request -- the request that was sent.
    cID     -- the course id
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [cID] = utils.required_params(request.data, 'cID')
    except KeyError:
        return responses.keyerror('cID')

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_edit_course_roles:
        return responses.forbidden('You cannot edit roles of this course.')

    for role in request.data['roles']:
        db_role = Role.objects.filter(name=role['name'], course__id=cID)
        if not db_role:
            factory.make_role_default_no_perms(role['name'], Course.objects.get(pk=cID), **role['permissions'])
        else:
            permissions.edit_permissions(db_role[0], **role['permissions'])
    return responses.success()


@api_view(['POST'])
def connect_assignment_lti(request):
    """Connect an existing assignment to an lti assignment.

    Arguments:
    request -- the update request that was send with
        aID -- the id of the assignment to be linked with lti
        lti_id -- lti_id that needs to be added to the assignment
        points_possible -- points_possible in lti assignment

    Returns a json string for if it is succesful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        aID, lti_id = utils.required_params(request.data, 'aID', 'lti_id')
        [points_possible] = utils.optional_params(request.data, 'points_possible')
    except KeyError:
        return responses.keyerror('aID')

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment')

    if not permissions.has_assignment_permission(user, assignment, 'can_edit_assignment'):
        return responses.forbidden('You are not allowed to edit the assignment.')

    assignment.lti_id = lti_id
    if assignment.points_possible is None and points_possible is not '':
        assignment.points_possible = points_possible
    assignment.save()

    return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
def update_course_with_student(request):
    """Update an existing course with a student.

    Arguments:
    request -- the update request that was send with
        uID -- student ID given with the request
        cID -- course ID given with the request

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        uID, cID = utils.required_params(request.data, 'uID', 'cID')
    except KeyError:
        return responses.keyerror('uID', 'cID')

    try:
        q_user = User.objects.get(pk=request.data['uID'])
        course = Course.objects.get(pk=request.data['cID'])
    except (User.DoesNotExist, Course.DoesNotExist):
        return responses.not_found('User, Course or Participation does not exist.')

    role = permissions.get_role(user, course)
    if role is None:
        return responses.forbidden('You are not in this course.')
    elif not role.can_add_course_participants:
        return responses.forbidden('You cannot add users to this course.')

    if permissions.is_user_in_course(q_user, course):
        return responses.bad_request('User already participates in the course.')

    role = Role.objects.get(name="Student", course=course)
    participation = factory.make_participation(q_user, course, role)

    assignments = course.assignment_set.all()

    role = permissions.get_role(q_user, cID)
    for assignment in assignments:
        if role.can_edit_journal:
            if not Journal.objects.filter(assignment=assignment, user=q_user).exists():
                factory.make_journal(assignment, q_user)

    participation.save()
    return responses.success(message='Succesfully added student to course')


@api_view(['POST'])
def update_assignment(request):
    """Update an existing assignment.

    Arguments:
    request -- the update request that was send with
        aID -- ID of the assignment
        name -- name of the assignment
        description -- description of the assignment

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        aID, name, description = utils.required_params(request.data, 'aID', 'name', 'description')
    except KeyError:
        return responses.keyerror('aID', 'name', 'description')

    try:
        assignment = Assignment.objects.get(pk=aID)
    except Assignment.DoesNotExist:
        return responses.not_found('Assignment')

    if not permissions.has_assignment_permission(user, assignment, 'can_edit_assignment'):
        return responses.forbidden('You are not allowed to edit this assignment.')

    assignment.name = request.data['name']
    assignment.description = request.data['description']
    assignment.save()

    return responses.success(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
def update_password(request):
    """Update a password.

    Arguments:
    request -- the update request that was send with
        new_password -- new password of the user
        old_password -- current password of the user

    Returns a json string for if it is successful or not.
    """
    user = request.user
    try:
        new_password, old_password = utils.required_params(request.data, 'new_password', 'old_password')
    except KeyError:
        return responses.KeyError('new_password', 'old_password')

    if not user.is_authenticated or not user.check_password(old_password):
        return responses.unauthorized('Wrong password.')

    if len(new_password) < 8:
        return responses.bad_request('Password needs to contain at least 8 characters.')
    if new_password == new_password.lower():
        return responses.bad_request('Password needs to contain at least 1 capital letter.')
    if re.match(r'^\w+$', new_password):
        return responses.bad_request('Password needs to contain a special character.')

    user.set_password(new_password)
    user.save()
    return responses.success(message='Succesfully changed the password.')


@api_view(['POST'])
def update_grade_notification(request):
    """Update whether the user gets notified when a grade changes/new grade.

    Arguments:
    request -- the request that was send with
        new_value -- the new value for the grade notifcation toggle

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [new_value] = utils.required_params(request.data, 'new_value')
    except KeyError:
        return responses.keyerror('new_value')

    user.grade_notifications = new_value
    user.save()

    return responses.success(payload={'new_value': user.grade_notifications})


@api_view(['POST'])
def update_comment_notification(request):
    """Update whether the user gets notified when a comment changes/new comment.

    Arguments:
    request -- the request that was send with

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [new_value] = utils.required_params(request.data, 'new_value')
    except KeyError:
        return responses.keyerror('new_value')

    user.comment_notifications = new_value
    user.save()
    return responses.success(payload={'new_value': user.comment_notifications})


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
def update_user_role_course(request):
    """Update user role in a course.

    Arguments:
    request -- the request that was send with
        role -- the new role for the user
        uID -- user id of the user to be updated
        cID -- the course of the new role

    Returns a json string for if it is successful or not.
    """
    try:
        role, uID, cID = utils.required_params(request.data, "role", "uID", "cID")
    except KeyError:
        return responses.keyerror("role", "uID", "cID")

    try:
        course = Course.objects.get(pk=cID)
        participation = Participation.objects.get(user=uID, course=cID)
    except (Participation.DoesNotExist, Role.DoesNotExist, Course.DoesNotExist):
        return responses.not_found('Participation, Role or Course does not exist.')

    q_role = permissions.get_role(request.user, course)
    if q_role is None:
        return responses.forbidden('You are not in this course.')
    elif not q_role.can_edit_course_roles:
        return responses.forbidden('You cannot edit the roles of this course.')

    participation.role = Role.objects.get(name=role, course=cID)

    participation.save()
    return responses.success(payload={'new_role': participation.role.name})


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

    if entry.published:
        EntryComment.objects.filter(entry_id=eID).update(published=True)

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

    if entry.published:
        EntryComment.objects.filter(entry_id=eID).update(published=True)

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
        return responses.forbidden('You are not allowed to publish journal grades.')

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
        ecID -- The ID of the entrycomment.
        text -- The updated text.
    Returns a json string for if it is successful or not.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        ecID, text = utils.required_params(request.data, "ecID", "text")
    except KeyError:
        return responses.keyerror("ecID")

    try:
        comment = EntryComment.objects.get(pk=ecID)
    except EntryComment.DoesNotExist:
        return responses.not_found('Entrycomment does not exist.')

    if not permissions.has_assignment_permission(request.user, comment.entry.node.journal.assignment,
                                                 'can_comment_journal'):
        return responses.forbidden('You cannot comment on entries.')

    comment.text = text
    comment.save()
    return responses.success()


@api_view(['POST'])
def update_user_file(request):
    """Update user profile picture.

    Arguments:
    request -- the update request that was send with
        is expected to contain a base64 encoded image.

    No validation is performed beyond a size check.

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    if not request.FILES or not request.FILES['file']:
        return responses.bad_request()

    try:
        validators.validate_user_file(request.FILES['file'])
    except ValidationError:
        return responses.bad_request('The selected file exceeds the file limit.')

    user_files = user.userfile_set.all()

    # Fast check for allowed user storage space
    if not ((USER_MAX_TOTAL_STORAGE_MB - (len(user_files) * USER_MAX_FILE_SIZE_MB)) * 1024 * 1024 >
            request.FILES['file'].size):
        # Slow check for allowed user storage space
        file_size_sum = 0
        for user_file in user_files:
            file_size_sum += user_file.file.size
        if file_size_sum > USER_MAX_TOTAL_STORAGE_MB * 1024 * 1024:
            return responses.bad_request('You have passed the user file storage limit.')

    user_file = factory.make_user_file(request.FILES['file'], user)

    return responses.fileb64(user_file)

    return responses.success()


@api_view(['POST'])
def update_user_profile_picture(request):
    """Update user profile picture.

    Arguments:
    request -- the update request that was send with
        is expected to contain a base64 encoded image.

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    if not request.data['urlData']:
        return responses.bad_request()

    validators.validate_profile_picture_base64(request.data['urlData'])

    user.profile_picture = request.data['urlData']
    user.save()

    return responses.success()


@api_view(['POST'])
def update_user_data(request):
    """Update user data.

    Arguments:
    request -- the update request that was send with
        username -- new password of the user
        picture -- current password of the user

    Returns a json string for if it is successful or not.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    if 'username' in request.data:
        username = request.data['username']
        if User.objects.filter(username=username).exists():
            return responses.bad_request('User with this username already exists.')
        user.username = username
    if 'picture' in request.data:
        user.profile_picture = request.data['picture']
    if 'first_name' in request.data:
        user.first_name = request.data['first_name']
    if 'last_name' in request.data:
        user.last_name = request.data['last_name']

    user.save()
    return responses.success(payload={'user': serialize.user_to_dict(user)})


@api_view(['POST'])
def update_lti_id_to_user(request):
    """Create a new user with lti_id.

    Arguments:
    request -- the request
        username -- username of the new user
        password -- password of the new user
        first_name -- first_name (optinal)
        last_name -- last_name (optinal)
        email -- email (optinal)
        jwt_params -- jwt params to get the lti information from
            user_id -- id of the user
            user_image -- user image
            roles -- role of the user
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    if not request.data['jwt_params']:
        return responses.bad_request()

    lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])

    user_id, user_image = lti_params['user_id'], lti_params['user_image']
    is_teacher = json.load(open('config.json'))['Teacher'] == lti_params['roles']
    first_name, last_name, email = utils.optional_params(request.data, 'first_name', 'last_name', 'email')

    if first_name is not None:
        user.first_name = first_name
    if last_name is not None:
        user.last_name = last_name
    if email is not None:
        if User.objects.filter(email=email).exists():
            return responses.bad_request('User with this email already exists.')

        user.email = email
    if user_image is not None:
        user.profile_picture = user_image
    if is_teacher:
        user.is_teacher = is_teacher

    if User.objects.filter(lti_id=user_id).exists():
        return responses.bad_request('User with this lti id already exists.')

    user.lti_id = user_id

    user.save()

    return responses.success(payload={'user': serialize.user_to_dict(user)})
