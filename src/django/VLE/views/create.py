"""
create.py.

API functions that handle the create requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from django.utils.timezone import now
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import VLE.serializers as serialize
import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.utils.email_handling as email_handling
from VLE.models import User, Journal, EntryTemplate, Node, Assignment, Field, Entry, Content, Course
import VLE.edag as edag
import VLE.lti_grade_passback as lti_grade
import VLE.validators as validators

import VLE.views.responses as responses
import VLE.permissions as permissions

import jwt
import json
from django.conf import settings


@api_view(['POST'])
def create_new_course(request):
    """Create a new course.

    Arguments:
    request -- the request that was send with
        name -- name of the course
        abbr -- abbreviation of the course
        startdate -- optional date when the course starts
        lti_id -- optional lti_id to link the course to

    On success, returns a json string containing the course.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    perm = permissions.get_permissions(user)

    if not perm["can_add_course"]:
        return responses.forbidden("You have no permissions to create a course.")

    try:
        name, abbr = utils.required_params(request.data, "name", "abbr")
        startdate, enddate, lti_id = utils.optional_params(request.data, "startdate", "enddate", "lti_id")
    except KeyError:
        return responses.keyerror("name", "abbr")

    course = factory.make_course(name, abbr, startdate, enddate, request.user, lti_id)

    return responses.created(payload={'course': serialize.course_to_dict(course)})


@api_view(['POST'])
def create_new_assignment(request):
    """Create a new assignment.

    Arguments:
    request -- the request that was send with
        name -- name of the assignment
        description -- description of the assignment
        cID -- id of the course the assignment belongs to

    On success, returns a json string containing the assignment.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        name, description, cID = utils.required_params(request.data, "name", "description", "cID")
        points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
    except KeyError:
        return responses.keyerror("name", "description", "cID")

    # Assignments can only be created with can_create_assignment permission.
    role = permissions.get_role(user, cID)
    if role is None:
        return responses.unauthorized("You have no access to this course.")
    elif not role.can_add_assignment:
        return responses.forbidden("You have no permissions to create a new assignment.")

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    assignment = factory.make_assignment(name, description, cIDs=[cID],
                                         author=request.user, lti_id=lti_id,
                                         points_possible=points_possible)

    try:
        course = Course.objects.get(pk=cID)
    except Course.DoesNotExist:
        return responses.not_found('Course does not exist.')

    for user in course.users.all():
        role = permissions.get_role(user, cID)
        if role.can_edit_journal:
            factory.make_journal(assignment, user)

    return responses.created(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
def create_journal(request):
    """Create a new journal.

    Arguments:
    request -- the request that was send with
    aID -- the assignment id

    On success, returns a json string containing the journal.
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        [aID] = utils.required_params(request.data, "aID")
    except KeyError:
        return responses.keyerror("aID")

    role = permissions.get_assignment_id_permissions(user, aID)

    if role == {}:
        return responses.forbidden("You have no permissions within this course.")
    elif not role["can_edit_journal"]:
        return responses.forbidden("You have no permissions to create a journal.")

    assignment = Assignment.objects.get(pk=aID)
    journal = factory.make_journal(assignment, request.user)

    return responses.created(payload={'journal': serialize.journal_to_dict(journal)})


@api_view(['POST'])
@parser_classes([JSONParser])
def create_entry(request):
    """Create a new entry.

    Arguments:
    request -- the request that was send with
    jID -- the journal id
    tID -- the template id to create the entry with
    nID -- optional: the node to bind the entry to (only for entrydeadlines)
    content -- the list of {tag, data} tuples to bind data to a template field.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        jID, tID, content_list = utils.required_params(request.data, "jID", "tID", "content")
        nID, = utils.optional_params(request.data, "nID")
    except KeyError:
        return responses.keyerror("jID", "tID", "content")

    try:
        journal = Journal.objects.get(pk=jID, user=request.user)

        template = EntryTemplate.objects.get(pk=tID)

        if nID:
            node = Node.objects.get(pk=nID, journal=journal)
            if node.type == Node.PROGRESS:
                return responses.bad_request('Passed node is a Progress node.')

            if node.entry:
                if node.entry.grade is None:
                    if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                        return responses.bad_request('The deadline has already passed.')

                    Content.objects.filter(entry=node.entry).all().delete()
                    node.entry.template = template
                    node.save()
                else:
                    return responses.bad_request('Can not overwrite entry, since it is already graded.')
            else:
                if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                    return responses.bad_request('The deadline has already passed.')

                node.entry = factory.make_entry(template)
                node.save()
        else:
            entry = factory.make_entry(template)
            node = factory.make_node(journal, entry)

        if journal.sourcedid is not None and journal.grade_url is not None:
            lti_grade.needs_grading(journal, node.id)

        for content in content_list:
            data = content['data']
            tag = content['tag']
            field = Field.objects.get(pk=tag)

            factory.make_content(node.entry, data, field)

        result = edag.get_nodes_dict(journal, request.user)
        added = -1
        for i, result_node in enumerate(result):
            if result_node['nID'] == node.id:
                added = i
                break

        return responses.created(payload={'added': added,
                                 'nodes': edag.get_nodes_dict(journal, request.user)})
    except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
        return responses.not_found('Journal, Template or Node does not exist.')


@api_view(['POST'])
def create_entrycomment(request):
    """Create a new entrycomment.

    Arguments:
    request -- the request that was send with
        eID -- the entry id
        uID -- the author id
        text -- the comment
        published -- the comment's publishment state
    """
    user = request.user
    if not user.is_authenticated:
        return responses.unauthorized()

    try:
        eID, uID, text, published = utils.required_params(request.data, "eID", "uID", "text", "published")
    except KeyError:
        return responses.keyerror("eID", "uID", "text", "published")

    try:
        author = User.objects.get(pk=uID)
        entry = Entry.objects.get(pk=eID)
        assignment = Assignment.objects.get(journal__node__entry=entry)
    except (User.DoesNotExist, Entry.DoesNotExist):
        return responses.not_found('User or Entry does not exist.')

    if not (author == user):
        return responses.forbidden('You are not allowed to write comments for others.')

    published = published or not permissions.has_assignment_permission(user, assignment, 'can_grade_journal')

    entrycomment = factory.make_entrycomment(entry, author, text, published)
    return responses.created(payload={'comment': serialize.entrycomment_to_dict(entrycomment)})


@api_view(['POST'])
def create_lti_user(request):
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
    if request.data['jwt_params'] is not '':
        try:
            lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
        except jwt.exceptions.ExpiredSignatureError:
            return responses.forbidden(
                description='The canvas link has expired, 15 minutes have passed. Please retry from canvas.')
        except jwt.exceptions.InvalidSignatureError:
            return responses.unauthorized(description='Invalid LTI parameters given. Please retry from canvas.')

        lti_id, user_image = lti_params['user_id'], lti_params['custom_user_image']
        is_teacher = json.load(open('config.json'))['Teacher'] in lti_params['roles']
    else:
        lti_id, user_image, is_teacher = None, None, False

    try:
        username, password = utils.required_params(request.data, 'username', 'password')
        first_name, last_name, email = utils.optional_params(request.data, 'first_name', 'last_name', 'email')
    except KeyError:
        return responses.keyerror('username', 'password')

    if User.objects.filter(email=email).exists():
        return responses.bad_request('User with this email address already exists.')

    if User.objects.filter(username=username).exists():
        return responses.bad_request('User with this username already exists.')

    if lti_id is not None and User.objects.filter(lti_id=lti_id).exists():
        return responses.bad_request('User with this lti id already exists.')

    try:
        validators.validate_password(password)
    except ValidationError as e:
        return responses.bad_request(e.args[0])

    try:
        validate_email(email)
    except ValidationError:
        return responses.bad_request('Invalid email address.')

    user = factory.make_user(username, password, email=email, lti_id=lti_id, is_teacher=is_teacher,
                             first_name=first_name, last_name=last_name, profile_picture=user_image,
                             verified_email=True if lti_id else False)

    if lti_id is None:
        email_handling.send_email_verification_link(user)

    return responses.created(description='User successfully created', payload={'user': serialize.user_to_dict(user)})
