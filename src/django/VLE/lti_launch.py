from django.conf import settings
import VLE.factory as factory
import oauth2
"""Package for oauth authentication in python"""

from VLE.models import User, Course, Assignment, Journal, Participation, Role


class OAuthRequestValidater(object):
    """OAuth request validater class for Django Requests"""

    def __init__(self, key, secret):
        """
        Constructor die een server en consumer object aanmaakt met de
        gegeven key en secret.
        """
        super(OAuthRequestValidater, self).__init__()
        self.consumer_key = key
        self.consumer_secret = secret

        self.oauth_server = oauth2.Server()
        signature_method = oauth2.SignatureMethod_HMAC_SHA1()
        self.oauth_server.add_signature_method(signature_method)
        self.oauth_consumer = oauth2.Consumer(
            self.consumer_key, self.consumer_secret
        )

    def parse_request(self, request):
        """
        Parses een django request om de method, url header en post data terug
        te geven.
        """
        headers = dict([(k, request.META[k])
                        for k in request.META if
                        k.upper().startswith('HTTP_') or
                        k.upper().startswith('CONTENT_')])

        return request.method, request.build_absolute_uri(), headers, \
            request.POST

    def is_valid(self, request):
        """
        Checks if the signature of the given request is valid based on the
        consumers secret en key
        """
        try:
            method, url, head, param = self.parse_request(request)

            oauth_request = oauth2.Request.from_request(
                method, url, headers=head, parameters=(param))

            oauth_request = oauth2.Request.from_request(
                request.method, request.build_absolute_uri(),
                headers=request.META, parameters=request.POST.dict()
            )
            self.oauth_server.verify_request(oauth_request,
                                             self.oauth_consumer, {})

        except (oauth2.Error, ValueError) as err:
            print(oauth_request['oauth_signature'])
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(),
                                       self.oauth_consumer, {})
            print(oauth_request['oauth_signature'])
            return False, err
        # Signature was valid
        return True, None

    @classmethod
    def check_signature(cls, key, secret, request):
        """
        Validates OAuth request using the python-oauth2 library:
            https://github.com/simplegeo/python-oauth2.
        """
        validator = OAuthRequestValidater(key, secret)
        return validator.is_valid(request)


def select_create_user(request):
    """
    Return the user of the lti_user_id in the request if it doesnt yet exist
    the user is create in our database.
    """
    lti_user_id = request['user_id']

    users = User.objects.filter(lti_id=lti_user_id)
    if users.count() > 0:
        user = users[0]
    else:
        user = User()
        if 'lis_person_contact_email_primary' in request:
            user.email = request['lis_person_contact_email_primary']

        if 'lis_person_sourcedid' in request:
            user.username = request['lis_person_sourcedid']

        if 'lis_person_name_full' in request:
            fullname = request['lis_person_name_full']
            splitname = fullname.split(' ')
            user.first_name = splitname[0]
            user.last_name = fullname[len(splitname[0])+1:]

        user.lti_id = lti_user_id
        user.save()

    if 'user_image' in request:
        user.profile_picture = request['user_image']
        user.save()

    return user


def create_lti_query_link(names, values):
    """
    Creates link to lti page with the given parameters

    Arguments
    -- names -> names of the query variables
    -- values -> values correnspanding to the names

    returns the link
    """
    link = settings.BASELINK
    link += '/LtiLaunch'
    start = '?'
    for i, name in enumerate(names):
        link += start + name + '={0}'.format(values[i])
        start = '&'
    return link


def check_course_lti(request, user, role):
    course_id = request['context_id']
    courses = Course.objects.filter(lti_id=course_id)

    if courses.count() > 0:
        course = courses[0]
        if user not in course.users.all():
            factory.make_participation(user, course, Role.objects.get(name=role))
        return course
    return None


def check_assignment_lti(request, user):
    assign_id = request['resource_link_id']
    assignments = Assignment.objects.filter(lti_id=assign_id)
    if assignments.count() > 0:
        return assignments[0]
    return None


def select_create_journal(request, user, assignment, roles):
    """
    Select or create the requested journal.
    """
    if roles['Student'] in request['roles'] and assignment is not None:
        journals = Journal.objects.filter(user=user, assignment=assignment)
        if journals.count() > 0:
            journal = journals[0]
        else:
            journal = factory.make_journal(assignment, user)

        if 'lis_outcome_service_url' in request:
            journal.grade_url = request['lis_outcome_service_url']
            journal.save()
        if 'lis_result_sourcedid' in request:
            journal.sourcedId = request['lis_result_sourcedid']
            journal.save()
    else:
        journal = None
    return journal
