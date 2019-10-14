import datetime
import test.factory as factory
from test.utils import api

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

import VLE.factory
import VLE.utils.generic_utils as utils
from VLE.models import Assignment, Course, Journal, Node, Role


class AssignmentAPITest(TestCase):
    def setUp(self):
        self.teacher = factory.Teacher()
        self.admin = factory.Admin()
        self.course = factory.Course(author=self.teacher)
        self.student = factory.Student()
        self.participating = factory.Participation(user=self.student, course=self.course)
        self.create_params = {
            'name': 'test',
            'description': 'test_description',
            'points_possible': 10,
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
        lti_params = {**self.create_params, **{'lti_id': 'new_lti_id'}}
        resp = api.create(self, 'assignments', params=lti_params, user=self.teacher)['assignment']
        assignment = Assignment.objects.get(pk=resp['id'])
        assert assignment.active_lti_id in assignment.lti_id_set, 'lti id should be set in the lti_id_set as well'
        assert assignment.active_lti_id in assignment.courses.first().assignment_lti_id_set, \
            'lti id should be set in the course assignment_lti_id_set as well'

        # Test creation with default params is not a group assignment
        assignment = api.create(self, 'assignments', params=self.create_params, user=self.teacher)['assignment']
        assert 'is_group_assignment' in assignment and not assignment['is_group_assignment'], \
            'Default assignment should be individual'
        assert 'group_size' not in assignment or assignment['group_size'] is None

        # Test required fields
        api.create(self, 'assignments', params={}, user=self.teacher, status=400)
        api.create(self, 'assignments', params={'name': 'test'}, user=self.teacher, status=400)
        api.create(self, 'assignments', params={'points_possible': 5}, user=self.teacher, status=400)

        # Test creation of group assignment
        params = {
            'name': 'test',
            'description': 'test_description',
            'points_possible': 10,
            'course_id': self.course.pk,
            'group_size': 3,
        }
        assignment = api.create(self, 'assignments', params=params, user=self.teacher)['assignment']
        assert 'is_group_assignment' in assignment and assignment['is_group_assignment'], \
            'Assignment with group size should be a group assignment'
        assert 'group_size' in assignment and assignment['group_size'] == 3

    def test_get(self):
        student = factory.Student()
        assignment = factory.Assignment(courses=[self.course])

        api.get(self, 'assignments', params={'pk': assignment.pk}, user=student, status=403)
        factory.Participation(
            user=student, course=self.course, role=Role.objects.get(course=self.course, name='Student'))
        resp = api.get(self, 'assignments', params={'pk': assignment.pk, 'course_id': self.course.pk},
                       user=student)['assignment']
        assert resp['journal'] is not None, 'Response should include student serializer'

        resp = api.get(self, 'assignments', params={'pk': assignment.pk, 'course_id': self.course.pk},
                       user=self.teacher)['assignment']
        assert resp['journals'] is not None, 'Response should include teacher serializer'

    def test_list(self):
        course2 = factory.Course(author=self.teacher)
        factory.Assignment(courses=[self.course])
        factory.Assignment(courses=[self.course, course2])
        assignment = factory.Assignment()

        resp = api.get(self, 'assignments', params={'course_id': self.course.pk}, user=self.teacher)['assignments']
        assert len(resp) == 2, 'All connected courses should be returned'
        resp = api.get(self, 'assignments', params={'course_id': course2.pk}, user=self.teacher)['assignments']
        assert len(resp) == 1, 'Not connected courses should not be returned'

        # Connected assignment
        course = assignment.courses.first()
        factory.Participation(user=self.teacher, course=course)
        # Not connected assignment
        factory.Assignment()

        resp = api.get(self, 'assignments', user=self.teacher)['assignments']
        assert len(resp) == 3, 'Without a course supplied, it should return all assignments connected to user'

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

    def test_lti_delete(self):
        assignment = factory.LtiAssignment()
        course = assignment.courses.first()
        assert assignment.active_lti_id in course.assignment_lti_id_set, \
            'assignment lti_id should be in assignment_lti_id_set of course before anything is deleted'
        # Test if deletion is possible to delete assignment if it has only one lti id
        api.delete(self, 'assignments', params={'pk': assignment.pk, 'course_id': course.pk}, user=factory.Admin())
        assert assignment.active_lti_id not in Course.objects.get(pk=course.pk).assignment_lti_id_set, \
            'assignment lti_id should get removed from the assignment_lti_id_set from the course'
        assignment = factory.LtiAssignment()
        course = assignment.courses.first()
        course2 = factory.LtiCourse()
        assignment.courses.add(course2)
        assignment.lti_id_set.append('second' + assignment.active_lti_id)
        assignment.save()
        # Test is deletion is not possible from connected LTI course
        api.delete(
            self, 'assignments', params={'pk': assignment.pk, 'course_id': course.pk}, user=factory.Admin(), status=400)
        # Test is deletion is possible from other course
        api.delete(
            self, 'assignments', params={'pk': assignment.pk, 'course_id': course2.pk}, user=factory.Admin())

    def test_copyable(self):
        teacher = factory.Teacher()
        course = factory.Course(author=teacher)
        assignment = factory.TemplateAssignment(courses=[course])
        factory.TemplateFormat(assignment=assignment)
        assignment2 = factory.TemplateAssignment(courses=[course])
        factory.TemplateFormat(assignment=assignment2)
        journal = factory.Journal(assignment=assignment2)
        [factory.Entry(node__journal=journal) for _ in range(4)]

        resp = api.get(self, 'assignments/copyable', params={'pk': assignment.pk}, user=teacher)['data']
        assert len(resp[0]['assignments']) == 1
        assert resp[0]['course']['id'] == course.id, 'copyable assignments should be displayed'

        before_id = api.get(self, 'formats', params={'pk': assignment2.pk},
                            user=teacher)['format']['templates'][0]['id']
        before_from_id = api.get(self, 'formats', params={'pk': assignment.pk},
                                 user=teacher)['format']['templates'][0]['id']
        resp = api.update(self, 'formats/copy', params={'pk': assignment2.pk, 'from_assignment_id': assignment.pk},
                          user=teacher)
        after_id = api.get(self, 'formats', params={'pk': assignment2.pk}, user=teacher)['format']['templates'][0]['id']

        after_from_id = api.get(self, 'formats', params={'pk': assignment.pk},
                                user=teacher)['format']['templates'][0]['id']
        assert before_id != after_id, 'Assignment should be changed'
        assert before_from_id == after_from_id, 'From assignment templates should be unchanged'

        assert len(utils.get_journal_entries(journal)) == 4, 'Old entries should not be removed'

    def test_upcoming(self):
        course2 = factory.Course(author=self.teacher)
        factory.Assignment(courses=[self.course])
        factory.Assignment(courses=[self.course, course2])
        assignment = factory.Assignment()

        resp = api.get(
            self, 'assignments/upcoming', params={'course_id': self.course.pk}, user=self.teacher)['upcoming']
        assert len(resp) == 2, 'All connected courses should be returned'
        resp = api.get(self, 'assignments/upcoming', params={'course_id': course2.pk}, user=self.teacher)['upcoming']
        assert len(resp) == 1, 'Not connected courses should not be returned'

        # Connected assignment
        course = assignment.courses.first()
        factory.Participation(user=self.teacher, course=course)
        # Not connected assignment
        factory.Assignment()

        resp = api.get(self, 'assignments/upcoming', user=self.teacher)['upcoming']
        assert len(resp) == 3, 'Without a course supplied, it should return all assignments connected to user'

        assignment.lock_date = timezone.now()
        assignment.save()
        resp = api.get(self, 'assignments/upcoming', user=self.teacher)['upcoming']
        assert len(resp) == 2, 'Past assignment should not be added'

    def test_lti_id_model_logic(self):
        # Test if a single lTI id can only be coupled to a singular assignment
        ltiAssignment1 = factory.LtiAssignment()
        ltiAssignment2 = factory.LtiAssignment()
        assert ltiAssignment1.active_lti_id != ltiAssignment2.active_lti_id, \
            'LTI ids of generated assignments should be unique.'

        ltiAssignment2.active_lti_id = ltiAssignment1.active_lti_id
        self.assertRaises(
            ValidationError,
            ltiAssignment2.save,
            msg='lti_id_set and assignment should be unique together for each arrayfield value'
        )

        assert ltiAssignment2.active_lti_id in ltiAssignment2.lti_id_set, \
            'LTI ids added to the assignment should als be added to the lti_id_set'

        journal = factory.Journal(assignment=ltiAssignment1)
        journal.grade_url = 'Not None'
        journal.sourcedid = 'Not None'
        journal.save()
        ltiAssignment1.active_lti_id = 'new lti id'
        ltiAssignment1.save()
        # Refresh the journal instance after the assignment update
        journal = Journal.objects.get(pk=journal.pk)

        assert journal.grade_url is None and journal.sourcedid is None, \
            'Updating the active LTI id of an assignment should reset the grade_url and sourcedid of all nested ' \
            'journals'

    def test_deadline(self):
        journal = factory.Journal(assignment__format=factory.TemplateFormatFactory())
        assignment = journal.assignment
        teacher = assignment.courses.first().author
        assignment.points_possible = 10

        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] == 'End of assignment', \
            'Default end of assignment should be shown'

        resp = api.get(self, 'assignments/upcoming', user=teacher)['upcoming']
        assert resp[0]['deadline']['date'] is None, \
            'Default no deadline for a teacher be shown'

        progress = VLE.factory.make_progress_node(assignment.format, timezone.now() + datetime.timedelta(days=3), 7)
        utils.update_journals(assignment.journal_set.all(), progress)

        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] == '0/7 points', \
            'When not having completed an progress node, that should be shown'

        entrydeadline = VLE.factory.make_entrydeadline_node(
            assignment.format, timezone.now() + datetime.timedelta(days=1), assignment.format.template_set.first())
        utils.update_journals(assignment.journal_set.all(), entrydeadline)

        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] == assignment.format.template_set.first().name, \
            'When not having completed an entry deadline, that should be shown'

        entry = factory.Entry(node=Node.objects.get(preset=entrydeadline))

        resp = api.get(self, 'assignments/upcoming', user=teacher)['upcoming']
        assert resp[0]['deadline']['date'] is not None, \
            'With ungraded entry a deadline for a teacher be shown'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 5, 'published': False}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=teacher)['upcoming']
        assert resp[0]['deadline']['date'] is not None, \
            'With only graded & NOT published entries a deadline for a teacher be shown'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 5, 'published': True}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=teacher)['upcoming']
        assert resp[0]['deadline']['date'] is None, \
            'With only graded & published entries no deadline for a teacher be shown'

        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] == '5/7 points', \
            'With only graded & published entries progres node should be the deadline'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 7, 'published': True}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] == 'End of assignment', \
            'With full points of progress node, end of assignment should be shown'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 10, 'published': True}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=journal.user)['upcoming']
        assert resp[0]['deadline']['name'] is None, \
            'With full points of assignment, no deadline should be shown'
