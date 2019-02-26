import test.factory as factory
from test.utils import api

from django.test import TestCase

import VLE.models


class ParticipationAPITest(TestCase):
    def setUp(self):
        self.teacher = factory.Teacher()
        self.course = factory.Course(author=self.teacher)
        factory.Assignment(courses=[self.course])
        participation = factory.Participation(course=self.course)
        self.student = participation.user
        # Username is 4 chartacters for the unenrolled check
        self.not_connected = factory.Student(username='4444', full_name='Not Connected')
        self.create_params = {'course_id': self.course.pk, 'user_id': self.not_connected.pk}
        self.group1 = factory.Group(course=self.course)
        self.group2 = factory.Group(course=self.course)
        self.update_params = {
            'pk': self.course.pk,
            'user_id': self.student.pk,
            'role': 'Teacher',
            'group': self.group1.name
        }

    def test_get(self):
        api.get(self, 'participations', params={'course_id': self.course.pk}, user=self.student, status=403)
        api.get(self, 'participations', params={'course_id': self.course.pk}, user=self.teacher)

        resp = api.get(self, 'participations', params={'pk': self.course.pk}, user=self.student)
        assert resp['participant']['user']['id'] == self.student.pk
        resp = api.get(self, 'participations', params={'pk': self.course.pk}, user=self.teacher)
        assert resp['participant']['user']['id'] == self.teacher.pk

    def test_create(self):
        api.create(self, 'participations', params=self.create_params, user=self.student, status=403)
        api.create(self, 'participations', params=self.create_params, user=self.teacher)

    def test_update(self):
        api.update(self, 'participations', params=self.update_params, user=self.student, status=403)

        resp = api.update(self, 'participations', params=self.update_params, user=self.teacher)
        assert resp['participation']['group']['name'] == self.update_params['group']

        # Check cannot update role without can_edit_course_roles permissions
        VLE.models.Role.objects.filter(course=self.course).update(can_edit_course_roles=False)
        self.update_params['group'] = self.group2.name
        api.update(self, 'participations', params=self.update_params, user=self.teacher, status=403)
        self.update_params.pop('role', None)
        resp = api.update(self, 'participations', params=self.update_params, user=self.teacher)
        assert resp['participation']['group']['name'] == self.update_params['group']

    def test_delete(self):
        api.delete(self, 'participations', params={'pk': self.course.pk}, user=self.teacher, status=400)
        api.delete(self, 'participations',
                   params={'pk': self.course.pk, 'user_id': self.student.pk}, user=self.student, status=403)
        api.delete(self, 'participations',
                   params={'pk': self.course.pk, 'user_id': self.student.pk}, user=self.teacher)
        api.delete(self, 'participations',
                   params={'pk': self.course.pk, 'user_id': self.student.pk}, user=self.teacher, status=404)

    def test_unenrolled(self):
        api.get(self, 'participations/unenrolled',
                params={'course_id': self.course.pk, 'unenrolled_query': ''}, user=self.student, status=403)
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': ''}, user=self.teacher)
        assert len(resp['participants']) == 0

        # Check perfect name that is small
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': self.not_connected.username},
                       user=self.teacher)
        assert len(resp['participants']) == 1

        # Check first and last name
        resp = api.get(self, 'participations/unenrolled',
                       params={
                           'course_id': self.course.pk,
                           'unenrolled_query': self.not_connected.full_name[:5] + ' ' + 'invalid_last_name'},
                       user=self.teacher)
        assert len(resp['participants']) == 0
        resp = api.get(self, 'participations/unenrolled',
                       params={
                           'course_id': self.course.pk,
                           'unenrolled_query': self.not_connected.full_name},
                       user=self.teacher)
        assert len(resp['participants']) == 1

        # Check subnames of longer names
        other_not_conn = factory.Student(username='longusername', full_name='longfirstname longlastname')
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': other_not_conn.full_name[:6]},
                       user=self.teacher)
        assert len(resp['participants']) == 1
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': other_not_conn.full_name[-6:]},
                       user=self.teacher)
        assert len(resp['participants']) == 1
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': other_not_conn.username[:6]},
                       user=self.teacher)
        assert len(resp['participants']) == 1

        # Check too small, not found
        resp = api.get(self, 'participations/unenrolled',
                       params={'course_id': self.course.pk, 'unenrolled_query': other_not_conn.full_name[:4]},
                       user=self.teacher)
        assert len(resp['participants']) == 0
