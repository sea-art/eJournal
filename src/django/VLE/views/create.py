"""
create.py.

API functions that handle the create requests.
"""
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from django.utils.timezone import now

import VLE.serializers as serialize
import VLE.factory as factory
import VLE.utils as utils
from VLE.models import User, Journal, EntryTemplate, Node, Assignment, Field, Entry, Content
import VLE.edag as edag
import VLE.lti_grade_passback as lti_grade

import VLE.views.responses as responses

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
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        name, abbr = utils.required_params(request.data, "name", "abbr")
        startdate, lti_id = utils.optional_params(request.data, "startdate", "lti_id")
    except KeyError:
        return responses.keyerror("name", "abbr")

    course = factory.make_course(name, abbr, startdate, request.user, lti_id)

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
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        name, description, cID = utils.required_params(request.data, "name", "description", "cID")
        points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
    except KeyError:
        return responses.keyerror("name", "description", "cID")

    assignment = factory.make_assignment(name, description, cIDs=[cID],
                                         author=request.user, lti_id=lti_id,
                                         points_possible=points_possible)

    return responses.created(payload={'assignment': serialize.assignment_to_dict(assignment)})


@api_view(['POST'])
def create_journal(request):
    """Create a new journal.

    Arguments:
    request -- the request that was send with
    aID -- the assignment id

    On success, returns a json string containing the journal.
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        [aID] = utils.required_params(request.data, "aID")
    except KeyError:
        return responses.keyerror("aID")

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

        if journal.sourcedid is not None and journal.grade_url is not None:
            lti_grade.needs_grading(journal)

        template = EntryTemplate.objects.get(pk=tID)

        # TODO: Check if node can still be created (deadline passed? graded?)
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
        entryID -- the entry id
        authorID -- the author id
        text -- the comment
    """
    if not request.user.is_authenticated:
        return responses.unauthorized()

    try:
        entryID, authorID, text = utils.required_params(request.data, "entryID", "authorID", "text")
    except KeyError:
        return responses.keyerror("entryID", "authorID", "text")

    try:
        author = User.objects.get(pk=authorID)
        entry = Entry.objects.get(pk=entryID)
    except (User.DoesNotExist, Entry.DoesNotExist):
        return responses.not_found('User or Entry does not exist.')

    entrycomment = factory.make_entrycomment(entry, author, text)
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
        lti_params = jwt.decode(request.data['jwt_params'], settings.LTI_SECRET, algorithms=['HS256'])
        user_id, user_image = lti_params['user_id'], lti_params['user_image']
        is_teacher = json.load(open('config.json'))['Teacher'] in lti_params['roles']
    else:
        user_id, user_image, is_teacher = None, None, False

    try:
        username, password = utils.required_params(request.data, 'username', 'password')
        first_name, last_name, email = utils.optional_params(request.data, 'first_name', 'last_name', 'email')
    except KeyError:
        return responses.keyerror('username', 'password')

    user = factory.make_user(username, password, email=email, lti_id=user_id, is_teacher=is_teacher,
                             first_name=first_name, last_name=last_name, profile_picture=user_image)

    return responses.created(message='User successfully created', payload={'user': serialize.user_to_dict(user)})
