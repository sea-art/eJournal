import test.factory as factory
from test.utils import api

from django.test import TestCase


class AssignmentAPITest(TestCase):
    def setUp(self):
        self.teacher = factory.Teacher()
        self.admin = factory.Admin()
        self.course = factory.Course(author=self.teacher)
        self.create_params = {
            'name': 'test',
            'description': 'test_description',
            'course_id': self.course.pk
        }

    def test_rest(self):
        # Test the basic rest functionality as a superuser
        api.test_rest(self, 'assignments',
                      create_params=self.create_params,
                      get_params={'course_id': self.course.pk},
                      update_params={'description': 'test_description2'},
                      delete_params={'course_id': self.course.pk},
                      user=factory.Admin())

        # Test the basic rest functionality as a teacher
        api.test_rest(self, 'assignments',
                      create_params=self.create_params,
                      get_params={'course_id': self.course.pk},
                      update_params={'description': 'test_description2'},
                      delete_params={'course_id': self.course.pk},
                      user=self.teacher)

        # Test the basic rest functionality as a student
        api.test_rest(self, 'assignments',
                      create_params=self.create_params,
                      create_status=403,
                      user=factory.Student())

    def test_create(self):
        # Test creation with default params is not a group assignment
        assignment = api.create(self, 'assignments', params=self.create_params, user=self.teacher)['assignment']
        assert not assignment['is_group_assignment'], 'Default assignment should be individual'

        # Test required fields
        api.create(self, 'assignments', params={}, user=self.teacher, status=400)
        api.create(self, 'assignments', params={'name': 'test'}, user=self.teacher, status=400)

        # Test creation of group assignment

    def test_update(self):
        assignment = api.create(self, 'assignments', params=self.create_params, user=self.teacher)['assignment']

        # Try to publish the assignment
        # TODO: Test cannot unpublish when there are entries inside
        api.update(self, 'assignments', params={'pk': assignment['id'], 'published': True},
                   user=factory.Student(), status=403)
        api.update(self, 'assignments', params={'pk': assignment['id'], 'published': True},
                   user=self.teacher)
        api.update(self, 'assignments', params={'pk': assignment['id'], 'published': True},
                   user=factory.Admin())

        # Test script sanitation
        params = {
            'pk': assignment['id'],
            'description': '<script>alert("asdf")</script>Rest'
        }
        resp = api.update(self, 'assignments', params=params, user=self.teacher)['assignment']
        assert resp['description'] != params['description']

    def test_delete(self):
        teach_course = factory.Course(author=self.teacher)
        other_course = factory.Course()
        assignment = factory.Assignment(courses=[self.course, teach_course, other_course])

        # Test no course specified
        api.delete(self, 'assignments', params={'pk': assignment.pk}, user=self.teacher, status=400)

        # Test normal removal
        resp = api.delete(self, 'assignments',
                          params={'pk': assignment.pk, 'course_id': teach_course.id}, user=self.teacher)
        assert 'removed' in resp['description'] and 'deleted' not in resp['description'], \
            'The assignment should be removed from the course, not deleted'

        # Test if only admins can delete assignments they are not part of
        resp = api.delete(self, 'assignments',
                          params={'pk': assignment.pk, 'course_id': other_course.id}, user=self.teacher, status=403)
        resp = api.delete(self, 'assignments',
                          params={'pk': assignment.pk, 'course_id': other_course.id}, user=self.teacher, status=403)
        resp = api.delete(self, 'assignments',
                          params={'pk': assignment.pk, 'course_id': other_course.id}, user=self.admin, status=200)

        # Test delete
        resp = api.delete(self, 'assignments',
                          params={'pk': assignment.pk, 'course_id': self.course.id}, user=self.teacher)
        assert 'removed' not in resp['description'] and 'deleted' in resp['description'], \
            'The assignment should be deleted from the course, not removed'

    def test_join(self):
        group_assignment = factory.GroupAssignment()
