"""
test_lti_launch.py.

Test lti launch.
"""

import datetime
import test.factory as factory
import time
from test.utils import api

import oauth2
from django.conf import settings
from django.test import RequestFactory, TestCase

import VLE.lti_launch as lti
import VLE.views.lti as lti_view
from VLE.models import Lti_ids, User

REQUEST = {
    'oauth_consumer_key': str(settings.LTI_KEY),
    'oauth_signature_method': 'HMAC-SHA1',
    'oauth_version': '1.0',
    'custom_assignment_due': '2018-11-10 23:59:00 +0100',
    'custom_assignment_id': 'assignment_lti_id',
    'custom_assignment_lock': '2018-12-15 23:59:59 +0100',
    'custom_assignment_title': 'Assignment Title',
    'custom_assignment_unlock': '2018-08-16 00:00:00 +0200',
    'custom_assignment_points': '10',
    'custom_assignment_publish': 'true',
    'custom_course_id': 'course_lti_id',
    'custom_course_name': 'Course Title',
    'custom_course_start': '2018-06-15 14:41:00 +0200',
    'context_label': 'aaaa',
    'lti_message_type': 'basic-lti-launch-request',
    'lti_version': 'LTI-1p0',
    'custom_username': 'custom_username',
    'roles': '',
    'custom_user_image': 'https://uvadlo-tes.instructure.com/images/thumbnails/11601/\
    6ivT7povCYWoXPCVOSnfPqWADsLktcGXTXkAUYDv',
    'user_id': 'invalid_student_lti_id',
    'oauth_timestamp': 'null',
    'oauth_nonce': 'null'
}


def get_signature(request):
    oauth_request = oauth2.Request.from_request('POST', 'http://testserver/lti/launch', parameters=request)
    oauth_consumer = oauth2.Consumer(settings.LTI_KEY, settings.LTI_SECRET)
    return oauth2.SignatureMethod_HMAC_SHA1().sign(oauth_request, oauth_consumer, {}).decode('utf-8')


def create_request(request_body={}, timestamp=str(int(time.time())), nonce=str(oauth2.generate_nonce()),
                   delete_field=False):
    request = REQUEST.copy()
    request['oauth_timestamp'] = timestamp
    request['oauth_nonce'] = nonce

    for key, value in request_body.items():
        if key != 'oauth_signature':
            request[key] = value

    if delete_field is not False:
        request.pop(delete_field, None)

    request['oauth_signature'] = get_signature(request)

    if 'oauth_signature' in request_body:
        request['oauth_signature'] = request_body['oauth_signature']

    return request


def lti_launch(request_body={}, response_value=lti_view.LTI_STATES.NO_USER.value, timestamp=str(int(time.time())),
               nonce=str(oauth2.generate_nonce()), status=302, assert_msg='',
               delete_field=False):

    request = create_request(request_body, timestamp, nonce, delete_field)
    request = RequestFactory().post('http://127.0.0.1:8000/lti/launch', request)
    response = lti_view.lti_launch(request)
    assert response.status_code == status
    assert 'state={0}'.format(response_value) in response.url, assert_msg
    return response


def get_jwt(obj, request_body={}, timestamp=str(int(time.time())), nonce=str(oauth2.generate_nonce()),
            user=None, status=200, response_msg='', assert_msg='', response_value=None, delete_field=False):
    request = create_request(request_body, timestamp, nonce, delete_field)
    jwt_params = lti_view.encode_lti_params(request)
    response = api.get(obj, '/get_lti_params_from_jwt/{0}/'.format(jwt_params), user=user, status=status)
    if response_msg:
        if 'description' in response:
            assert response_msg in response['description'], assert_msg
        else:
            assert response_msg in response['detail'], assert_msg
    elif response_value:
        assert response['params']['state'] in response_value, assert_msg
    return response


class LtiLaunchTest(TestCase):
    """Lti launch test.

    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        """Setup."""
        self.factory = RequestFactory()

        self.new_lti_id = 'new_lti_id'

        self.teacher = factory.Teacher()
        self.teacher.lti_id = 'teacher_lti_id'
        self.teacher.save()

        self.student = factory.Student()
        self.student.lti_id = 'student_lti_id'
        self.student.save()
        self.request = REQUEST.copy()

        self.journal = factory.Journal(authors=[self.student])
        self.assignment = self.journal.assignment

    def test_select_user(self):
        selected_user = lti.get_user_lti({'user_id': self.student.lti_id})
        assert selected_user == self.student, 'get_user_lti should return a user when given an lti_id'

    def test_lti_launch_no_user_no_info(self):
        lti_launch(
            assert_msg='Without anything, it should give redirect msg with state = NO_USER'
        )

    def test_lti_launch_no_user(self):
        lti_launch(
            request_body={
                'custom_user_full_name': 'testpersoon voor Science',
                'custom_username': 'TestUser',
                'custom_user_email': 'ltiTest@test.com'
            },
            assert_msg='Without a user lti_id, it should give redirect msg with state = NO_USER',
        )

    def test_lti_launch_user(self):
        lti_launch(
            request_body={
                'user_id': self.student.lti_id
            },
            response_value=lti_view.LTI_STATES.LOGGED_IN.value,
            assert_msg='With a user_id the user should login',
        )

    def test_lti_launch_multiple_roles(self):
        lti_launch(
            request_body={
                'roles': 'Learner,Instructor',
                'user_id': self.student.lti_id
            },
            response_value=lti_view.LTI_STATES.LOGGED_IN.value,
            assert_msg='With a user_id the user should login',
        )
        assert User.objects.filter(lti_id=self.student.lti_id)[0].is_teacher, \
            'Student should become a teacher when loggin in with Instructor role'

    def test_lti_launch_unknown_role(self):
        lti_launch(
            request_body={
                'roles': 'urn:lti:instrole:ims/lis/Administrator',
                'user_id': self.student.lti_id
            },
            response_value=lti_view.LTI_STATES.LOGGED_IN.value,
            assert_msg='With an invalid role the user should still login',
        )

    def test_lti_launch_wrong_signature(self):
        lti_launch(
            request_body={
                'roles': 'urn:lti:instrole:ims/lis/Administrator',
                'user_id': self.new_lti_id,
                'oauth_signature': 'invalid'
            },
            response_value=lti_view.LTI_STATES.BAD_AUTH.value,
            assert_msg='With an invalid signature, a user should not be able to login',
        )

    def test_lti_launch_key_error(self):
        lti_launch(
            request_body={
                'user_id': self.new_lti_id
            },
            response_value=lti_view.LTI_STATES.KEY_ERR.value,
            assert_msg='Without all the keys, it should return a KEY_ERROR',
            delete_field='custom_username',
        )

    def test_get_lti_params_from_invalid_user_id(self):
        get_jwt(
            self, user=self.student, status=404,
            request_body={'user_id': 'invalid_user_id'},
            response_msg='User does not exist',
            assert_msg='Without a valid lti_id it should not find the user')

    def test_get_lti_params_from_jwt_wrong_user(self):
        get_jwt(
            self, user=self.teacher, status=403,
            request_body={'user_id': self.student.lti_id},
            response_msg='The user specified that should be logged in according',
            assert_msg='With an lti_id from another user, it should return forbidden')

    def test_get_lti_params_from_jwt_unauthorized(self):
        get_jwt(
            self, user=None, status=401,
            request_body={'user_id': self.student.lti_id},
            response_msg='Authentication credentials were not provided.',
            assert_msg='User needs to be logged in before the user can extract lti_params')

    def test_get_lti_params_from_jwt_expired(self):
        get_jwt(
            self, user=self.student, status=403,
            request_body={
                'user_id': self.student.lti_id,
                'exp': datetime.datetime.utcnow() - datetime.timedelta(minutes=30)
            },
            response_msg='expired',
            assert_msg='App should return expired if experation time is past')

    def test_get_lti_params_from_jwt_course_teacher(self):
        get_jwt(
            self, user=self.teacher, status=200,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'Instructor'},
            response_value=lti_view.LTI_STATES.NEW_COURSE.value,
            assert_msg='When a teacher gets jwt_params for the first time it should return the NEW_COURSE state')

    def test_get_lti_params_from_jwt_course_student(self):
        get_jwt(
            self, user=self.student, status=404,
            request_body={'user_id': self.student.lti_id},
            response_msg='not finished setting up the course',
            assert_msg='When a student gets jwt_params and the course is not setup, it should return response_msg')

    def test_get_lti_params_from_jwt_assignment_teacher(self):
        factory.LtiCourse(author=self.teacher, name=REQUEST['custom_course_name'])
        get_jwt(
            self, user=self.teacher, status=200,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'Instructor',
                'custom_course_id': Lti_ids.objects.filter(course__author=self.teacher).first().lti_id},
            response_value=lti_view.LTI_STATES.NEW_ASSIGN.value,
            assert_msg='When a teacher gets jwt_params after course is created it should return the NEW_ASSIGN state')

    def test_get_lti_params_from_jwt_no_context_label(self):
        get_jwt(
            self, user=self.teacher, status=200,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'Instructor'},
            response_value=lti_view.LTI_STATES.NEW_COURSE.value,
            delete_field='context_label')

    def test_get_lti_params_from_jwt_assignment_student(self):
        factory.LtiCourse(author=self.teacher, name=REQUEST['custom_course_name'])
        get_jwt(
            self, user=self.student, status=404,
            request_body={
                'user_id': self.student.lti_id,
                'custom_course_id': Lti_ids.objects.filter(course__author=self.teacher).first().lti_id},
            response_msg='not finished setting up the assignment',
            assert_msg='When a student gets jwt_params after course is created it should return response_msg')

    def test_get_lti_params_from_jwt_journal_teacher(self):
        course = factory.LtiCourse(author=self.teacher, name=REQUEST['custom_course_name'])
        factory.LtiAssignment(author=self.teacher, courses=[course], name=REQUEST['custom_assignment_title'])
        get_jwt(
            self, user=self.teacher, status=200,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'Instructor',
                'custom_course_id': Lti_ids.objects.filter(course__author=self.teacher).first().lti_id,
                'custom_assignment_id': Lti_ids.objects.filter(assignment__author=self.teacher).first().lti_id},
            response_value=lti_view.LTI_STATES.FINISH_T.value,
            assert_msg='When after assignment is created it should return the FINISH_T state for teachers')

    def test_get_lti_params_from_jwt_journal_student(self):
        course = factory.LtiCourse(author=self.teacher, name=REQUEST['custom_course_name'])
        factory.LtiAssignment(author=self.teacher, courses=[course], name=REQUEST['custom_assignment_title'])
        get_jwt(
            self, user=self.student, status=200,
            request_body={
                'user_id': self.student.lti_id,
                'custom_course_id': Lti_ids.objects.filter(course__author=self.teacher).first().lti_id,
                'custom_assignment_id': Lti_ids.objects.filter(assignment__author=self.teacher).first().lti_id},
            response_value=lti_view.LTI_STATES.FINISH_S.value,
            assert_msg='When after assignment is created it should return the FINISH_S state for students')

    def test_get_lti_params_from_jwt_multiple_roles(self):
        get_jwt(
            self, user=self.student, status=200,
            request_body={
                'user_id': self.student.lti_id,
                'roles': 'Learner,Instructor'},
            response_value=lti_view.LTI_STATES.NEW_COURSE.value,
            assert_msg='When a student tries to create a new course, with also a new Instructor role, \
                        it should grand its permissions')

    def test_get_lti_params_from_jwt_unknown_role(self):
        get_jwt(
            self, user=self.teacher, status=404,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'urn:lti:instrole:ims/lis/Administrator'},
            response_msg='not finished setting up the course',
            assert_msg='When a teacher goes to the platform without a teacher role, it should lose its teacher powers')

    def test_get_lti_params_from_jwt_key_Error(self):
        get_jwt(
            self, user=self.teacher, status=400,
            request_body={
                'user_id': self.teacher.lti_id,
                'roles': 'Instructor'},
            delete_field='custom_course_id',
            response_msg='missing',
            assert_msg='When missing keys, it should return a keyerror')

    def test_select_course_with_participation(self):
        """Hopefully select a course."""
        course = factory.LtiCourse(author=self.teacher, name=REQUEST['custom_course_name'])
        selected_course = lti.update_lti_course_if_exists(
            {'custom_course_id': Lti_ids.objects.filter(course=course).last().lti_id},
            user=self.teacher, role=settings.ROLES['Teacher'])
        assert selected_course == course

    def test_select_journal(self):
        """Hopefully select a journal."""
        selected_journal = lti.select_create_journal(
            {
                'roles': settings.ROLES['Student'],
                'lis_result_sourcedid': "267-686-2694-585-0afc8c37342732c97b011855389af1f2c2f6d552",
                'lis_outcome_service_url': "https://uvadlo-tes.instructure.com/api/lti/v1/tools/267/grade_passback"
            },
            user=self.student,
            assignment=self.assignment
        )
        assert selected_journal == self.journal

    def test_select_journal_no_assign(self):
        """Hopefully select None."""
        selected_journal = lti.select_create_journal(
            {
                'roles': settings.ROLES['Student'],
                'lis_result_sourcedid': "267-686-2694-585-0afc8c37342732c97b011855389af1f2c2f6d552",
                'lis_outcome_service_url': "https://uvadlo-tes.instructure.com/api/lti/v1/tools/267/grade_passback"
            },
            user=self.student,
            assignment=None
        )
        assert selected_journal is None
