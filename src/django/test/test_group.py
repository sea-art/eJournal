import test.factory as factory
from test.utils import api
from test.utils.response import in_response

from django.test import TestCase

import VLE.factory as nfac
from VLE.models import Group


class GroupAPITest(TestCase):
    def setUp(self):
        self.teacher = factory.Teacher()
        self.course = factory.Course(author=self.teacher)
        self.create_params = {'name': 'test', 'course_id': self.course.pk}
        self.group = factory.Group(course=self.course)

    def test_rest(self):
        # Test the basic rest functionality as a superuser
        api.test_rest(self, 'groups',
                      create_params=self.create_params,
                      get_params={'course_id': self.course.pk}, get_status=405, get_is_create=False,
                      update_params={'name': 'test2'},
                      user=factory.Admin())

        # Test the basic rest functionality as a teacher
        api.test_rest(self, 'groups',
                      create_params=self.create_params,
                      get_params={'course_id': self.course.pk}, get_status=405, get_is_create=False,
                      update_params={'name': 'test2'},
                      user=self.teacher)

        # Test the basic rest functionality as a student
        api.test_rest(self, 'groups',
                      create_params=self.create_params, get_status=405, get_is_create=False,
                      create_status=403,
                      user=factory.Student())

    def test_get(self):
        # Test all groups from course
        api.get(self, 'groups', user=self.teacher, status=400)
        api.get(self, 'groups', params={'course_id': self.course.pk}, user=factory.Student(), status=403)
        api.get(self, 'groups', params={'course_id': self.course.pk}, user=factory.Admin())
        get_resp = api.get(self, 'groups', params={'course_id': self.course.pk}, user=self.teacher)['groups']
        assert in_response(get_resp, self.group), 'Group that is added to  the course, should also be returned'

    def test_create(self):
        # Test required params
        api.create(self, 'groups', user=self.teacher, status=400)

        # Test connected teacher
        resp = api.create(self, 'groups',
                          params={'course_id': self.course.pk, 'name': 'Test', 'lti_id': 'lti'}, user=self.teacher)
        assert resp['group']['name'] == 'Test'

        # Test unconnected admin
        api.create(self, 'groups', params={'course_id': self.course.pk, 'name': 'Test2'}, user=factory.Admin())

        # Test duplicate
        api.create(self, 'groups', params={'course_id': self.course.pk, 'name': 'Test', 'lti_id': 'lti'},
                   user=self.teacher, status=400)

        # Test not authorized teacher
        api.create(self, 'groups', params={'course_id': self.course.pk, 'name': 'Test'},
                   user=factory.Teacher(), status=403)

        # Test student
        api.create(self, 'groups', params={'course_id': self.course.pk, 'name': 'Test'},
                   user=factory.Student(), status=403)

    def test_update(self):
        # Test required params
        api.update(self, 'groups', params={'pk': self.group.pk}, user=factory.Admin(), status=400)

        # Test unconnected admin
        resp = api.update(self, 'groups', params={'pk': self.group.pk, 'name': 'Test2'}, user=factory.Admin())
        assert resp['group']['name'] == 'Test2'

        # Test duplicate
        factory.Group(name='duplicate', course=self.course)
        factory.Group(name='other_duplicate')
        api.update(self, 'groups', params={'pk': self.group.pk, 'name': 'duplicate'}, user=factory.Admin())
        api.update(self, 'groups', params={'pk': self.group.pk, 'name': 'other_duplicate'}, user=factory.Admin())

    def test_delete(self):
        api.delete(self, 'groups', params={'pk': self.group.pk}, user=factory.Student(), status=403)
        api.delete(self, 'groups', params={'pk': self.group.pk}, user=factory.Teacher(), status=403)
        api.delete(self, 'groups', params={'pk': self.group.pk}, user=factory.Admin())

    def test_members(self):
        members = api.get(self, 'members', params={'group_id': self.group.pk}, user=self.teacher)['members']
        assert len(members) == 0, 'Default there should be 0 members in a group'

        api.create(self, 'members',
                   params={'group_id': self.group.pk, 'user_id': self.teacher.pk}, user=self.teacher)

        members = api.get(self, 'members', params={'group_id': self.group.pk}, user=self.teacher)['members']
        assert len(members) == 1, 'Teacher should be added to the group'

        members = api.delete(self, 'members',
                             params={'pk': self.group.pk, 'user_id': self.teacher.pk},
                             user=self.teacher)

        members = api.get(self, 'members', params={'group_id': self.group.pk}, user=self.teacher)['members']
        assert len(members) == 0, 'Teacher should be removed from the group'

        # Check not viewable for students
        api.delete(self, 'members',
                   params={'pk': self.group.pk, 'user_id': self.teacher.pk}, user=factory.Student(), status=403)
        api.create(self, 'members',
                   params={'group_id': self.group.pk, 'user_id': self.teacher.pk}, user=factory.Student(), status=403)
        api.get(self, 'members', params={'group_id': self.group.pk}, user=factory.Student(), status=403)

    def test_group_api(self):
        course = factory.Course(active_lti_id='6068')
        nfac.make_lti_groups(course)
        assert Group.objects.filter(course=course).count() > 0
