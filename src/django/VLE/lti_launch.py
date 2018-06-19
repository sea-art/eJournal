from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from urllib.parse import quote
import oauth2
import json
from datetime import datetime

from .models import User, Course, Assignment, Participation, Role, Journal


def dec_to_hex(dec):
    """Change int to hex value"""
    return hex(dec).split('x')[-1]


class OAuthRequestValidater(object):
    """
    OAuth request validater class for Django Requests
    """

    def __init__(self, key, secret):
        """
        Constructor die een server en consumer object aan maakt met de gegeven
        key en secret
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

        return request.method, request.build_absolute_uri(), headers, request.POST

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
            oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), self.oauth_consumer, {})
            print(oauth_request['oauth_signature'])
            return False, err
        # Signature was valid
        return True, None


def check_signature(key, secret, request):
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

        user.lti_id = lti_user_id
        user.save()

    return user


def select_create_course(request, user, roles):
    """
    Select or create a course requested.
    """
    course_id = request['context_id']
    courses = Course.objects.filter(lti_id=course_id)

    if courses.count() > 0:
        # If course already exists, select it.
        course = courses[0]

        if user not in course.participations.all():
            # If the user is not a participant, add a participation link with
            # the correct role given by the lti request.
            lti_roles = dict((roles[k], k) for k in roles)

            # Add the logged in user to the course through participation.
            # TODO Check if a teacher role already exists before adding it.
            role = Role.objects.create(name=lti_roles[request['roles']])
            Participation.objects.create(user=user, course=course, role=role)
    else:
        if roles['teacher'] in request['roles']:
            course = Course()
            course.name = request['context_title']
            course.abbreviation = request['context_label']
            course.lti_id = course_id
            course.startdate = datetime.now()
            course.save()

            # Add the logged in user to the course through participation.
            role = Role.objects.create(name='teacher')
            Participation.objects.create(user=user, course=course, role=role)

        else:
            # TODO redirect to unauthorized page
            return None

    return course


def select_create_assignment(request, user, course, roles):
    """
    Select or create a assignment requested.
    """
    assign_id = request['resource_link_id']
    assignments = Assignment.objects.filter(lti_id=assign_id)
    if assignments.count() > 0:
        # If the assigment exists, select it and add the course if necessary.
        assignment = assignments[0]
        if course not in assignment.courses.all():
            assignment.courses.add(course)

    else:
        # Try to create assignment.
        if roles['teacher'] in request['roles']:
            # If user is a teacher, create the assignment.
            assignment = Assignment()
            assignment.name = request['resource_link_title']
            assignment.lti_id = assign_id
            if 'custom_canvas_assignment_points_possible' in request:
                assignment.points_possible = request[
                    'custom_canvas_assignment_points_possible']
            assignment.save()
            assignment.courses.add(course)
        else:
            # TODO redirect to unauthorized page
            return None

    return assignment


def select_create_journal(request, user, assignment, roles):
    """
    Select or create the requested journal.
    """
    if roles['student'] in request['roles']:
        journals = Journal.objects.filter(user=user, assignment=assignment)
        if journals.count() > 0:
            journal = journals[0]
        else:
            journal = Journal()
            journal.assignment = assignment
            journal.user = user
            journal.save()
    else:
        journal = None
    return journal


@csrf_exempt
@xframe_options_exempt
def lti_launch(request):
    """Django view for the lti post request."""
    if request.method == 'POST':
        # canvas TODO change to its own database based on the key in the request.
        secret = '4339900ae5861f3086861ea492772864'
        key = '0cd500938a8e7414ccd31899710c98ce'

        print('key = postkey', key == request.POST['oauth_consumer_key'])
        authicated, err = check_signature(key, secret, request)

        if authicated:
            # Select or create the user, course, assignment and journal.
            roles = json.load(open('config.json'))
            user = select_create_user(request.POST, roles)
            course = select_create_course(request.POST, user, roles)
            assignment = select_create_assignment(request.POST, user, course, roles)
            journal = select_create_journal(request.POST, user, assignment, roles)

            # Check if the request comes from a student or not.
            roles = json.load(open('config.json'))
            student = request.POST['roles'] == roles['student']

            token = TokenObtainPairSerializer.get_token(user)
            access = token.access_token

            # Set the ID's or if these do not exist set them to undefined.
            cID = course.pk if course is not None else 'undefined'
            aID = assignment.pk if assignment is not None else 'undefined'
            jID = journal.pk if journal is not None else 'undefined'

            # TODO Should not be localhost anymore at production.
            link = 'http://localhost:8080/#/lti/launch'
            link += '?jwt_refresh={0}'.format(token)
            link += '&jwt_access={0}'.format(access)
            link += '&cID={0}'.format(cID)
            link += '&aID={0}'.format(aID)
            link += '&jID={0}'.format(jID)
            link += '&student={0}'.format(student)

            return redirect(link)
        else:
            return HttpResponse('unsuccesfull auth, {0}'.format(err))

        # Prints de post parameters als http page
        # TODO Remove these 2 lines
        post = json.dumps(request.POST, separators=(',', ': '))
        return HttpResponse(post.replace(',', ' <br> '))

    return HttpResponse('Hello, world.')
