from datetime import datetime, timezone

import oauth2
from django.conf import settings

import VLE.factory as factory
import VLE.utils.generic_utils as utils
from VLE.models import Group, Journal, Lti_ids, Participation, Role, User


class OAuthRequestValidater(object):
    """OAuth request validater class for Django Requests"""

    def __init__(self, key, secret):
        """
        Constructor which creates a consumer object with the given key and
        secret.
        """
        super(OAuthRequestValidater, self).__init__()
        self.consumer_key = key
        self.consumer_secret = secret

        self.oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        self.oauth_server.add_signature_method(signature_method)
        self.oauth_consumer = oauth2.Consumer(self.consumer_key, self.consumer_secret)

    def parse_request(self, request):
        """
        Parses a django request to return the method, url, header and post data.
        """
        return request.method, request.build_absolute_uri(), request.META, request.POST.dict()

    def is_valid(self, request):
        """
        Checks if the signature of the given request is valid based on the
        consumers secret en key
        """
        method, url, head, param = self.parse_request(request)
        oauth_request = oauth2.Request.from_request(method, url, headers=head, parameters=param)
        self.oauth_server.verify_request(oauth_request, self.oauth_consumer, {})

    @classmethod
    def check_signature(cls, key, secret, request):
        """Validate OAuth request using the python-oauth2 library.

        https://github.com/simplegeo/python-oauth2.
        """
        validator = OAuthRequestValidater(key, secret)
        validator.is_valid(request)


def roles_to_list(params):
    roles = list()
    if 'roles' in params:
        for role in params['roles'].split(','):
            roles.append(role.split('/')[-1].lower())
    return roles


def roles_to_lti_roles(lti_params):
    return [settings.LTI_ROLES[r] if r in settings.LTI_ROLES else r for r in roles_to_list(lti_params)]


def get_user_lti(request):
    """Check if a user with the lti_id exists"""
    lti_user_id = request['user_id']

    users = User.objects.filter(lti_id=lti_user_id)
    if users.count() > 0:
        user = users[0]
        if 'custom_user_image' in request:
            user.profile_picture = request['custom_user_image']
            user.save()

        if 'roles' in request and settings.ROLES['Teacher'] in roles_to_list(request):
            user.is_teacher = True
            user.save()
        return user
    return None


def create_lti_query_link(query):
    """
    Creates link to lti page with the given parameters

    Arguments
    query -- QueryDict of the query variables

    returns the link
    """
    return ''.join((settings.BASELINK, '/LtiLogin', '?', query.urlencode()))


def add_groups_if_not_exists(participation, group_ids):
    """Add the lti groups to a participant.

    This will only be done if there are no other groups already bound to the participant.
    """
    if participation.groups:
        return False

    for group_id in group_ids:
        group = Group.objects.filter(lti_id=group_id, course=participation.course)
        if group.exists():
            participation.groups.add(group.first())
        else:
            group = factory.make_course_group(group_id, participation.course, group_id)
            participation.groups.add(group)

    participation.save()
    return participation.groups


def _make_lti_participation(user, course, lti_role):
    """Make the user a participant in the course.

    This function also adds the role if this is a valid role registered in our system.
    """
    for role in settings.ROLES:
        if role in lti_role:
            return factory.make_participation(user, course, Role.objects.get(name=role, course=course))
    return factory.make_participation(user, course, Role.objects.get(name='Student', course=course))


def update_lti_course_if_exists(request, user, role):
    """Update a course with lti request.

    If no course exists, return None
    If it does exist:
    1. Put the user in the course
    2. Add groups to the user
    """
    course_lti_id = request.get('custom_course_id', None)
    lti_couple = Lti_ids.objects.filter(lti_id=course_lti_id, for_model=Lti_ids.COURSE)
    if course_lti_id is None or not lti_couple.exists():
        return None

    course = lti_couple.first().course

    # If the user not is a participant, add participation with possibly the role given by the LTI instance.
    if not user.is_participant(course):
        participation = _make_lti_participation(user, course, role)
    else:
        participation = Participation.objects.get(course=course, user=user)

    group_ids, = utils.optional_params(request, 'custom_section_id')
    if group_ids:
        add_groups_if_not_exists(participation, group_ids.split(','))

    return course


def update_lti_assignment_if_exists(request):
    """Update a course with lti request.

    If no course exists, return None
    If it does exist:
    Update the published state
    """
    assign_id = request['custom_assignment_id']
    lti_couples = Lti_ids.objects.filter(lti_id=assign_id, for_model=Lti_ids.ASSIGNMENT)
    if not lti_couples.exists():
        return None

    assignment = lti_couples.first().assignment
    if 'custom_assignment_publish' in request:
        assignment.is_published = request['custom_assignment_publish']
        assignment.save()
    return assignment


def select_create_journal(request, user, assignment):
    """
    Select or create the requested journal.
    """
    if assignment is None or user is None:
        return None

    within_assignment_timeframe = False
    try:
        begin = datetime.strptime(request['custom_assignment_unlock'], '%Y-%m-%d %X %z')
        end = datetime.strptime(request['custom_assignment_lock'], '%Y-%m-%d %X %z')
        now = datetime.now(timezone.utc)
        within_assignment_timeframe = begin < now < end
    except (ValueError, KeyError):
        pass

    journals = Journal.objects.filter(authors__in=[user], assignment=assignment)
    if journals.exists():
        journal = journals.first()
        if within_assignment_timeframe and 'lis_outcome_service_url' in request:
            journal.grade_url = request['lis_outcome_service_url']
            journal.save()
        return journal
    elif within_assignment_timeframe:
        journal = factory.make_journal(assignment, user)
        if 'lis_result_sourcedid' in request:
            journal.sourcedids.add(request['lis_result_sourcedid'])
            journal.save()
        if 'lis_outcome_service_url' in request:
            journal.grade_url = request['lis_outcome_service_url']
            journal.save()
        return journal

    return None
