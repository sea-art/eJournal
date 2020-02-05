import datetime
import test.factory as factory
from test.utils import api
from test.utils.generic_utils import equal_models

import pytest
from dateutil import parser
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import timezone

import VLE.factory
import VLE.utils.generic_utils as utils
from VLE.models import (Assignment, AssignmentParticipation, Course, Entry, Format, Journal, Node, Participation,
                        PresetNode, Role, Template)
from VLE.serializers import AssignmentSerializer
from VLE.utils.error_handling import VLEParticipationError
from VLE.views.assignment import day_neutral_datetime_increment, set_assignment_dates


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
            'is_group_assignment': True,
        }
        assignment = api.create(self, 'assignments', params=params, user=self.teacher)['assignment']
        assert 'is_group_assignment' in assignment and assignment['is_group_assignment'], \
            'Assignment with group size should be a group assignment'

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

        # Check group assignment
        group_assignment = factory.GroupAssignment()
        student = factory.AssignmentParticipation(assignment=group_assignment).user
        api.get(self, 'assignments', params={'pk': group_assignment.pk}, user=student)

    def test_get_assignment_with_given_course(self):
        assignment = factory.Assignment()
        course1 = assignment.courses.first()
        factory.Journal(assignment=assignment)
        course2 = factory.Course()
        assignment.courses.add(course2)
        factory.Journal(assignment=assignment)
        result = AssignmentSerializer(assignment, context={
            'user': course2.author, 'course': course2, 'journals': True}).data
        assert len(result['journals']) == 1, 'Course2 is supplied, only journals from that course should appear (1)'

        result = AssignmentSerializer(assignment, context={
            'user': course2.author, 'journals': True}).data
        assert not result['journals'], 'No course supplied should also return no journals'

        result = AssignmentSerializer(assignment, context={
            'user': course1.author, 'course': course1, 'journals': True}).data
        assert len(result['journals']) == 2, 'Course1 is supplied, only journals from that course should appear (2)'

        # Should not work when user is not in supplied course
        with pytest.raises(VLEParticipationError):
            result = AssignmentSerializer(assignment, context={
                'user': course2.author, 'course': course1, 'journals': True}).data

    def test_assigned_assignment(self):
        assignment = factory.Assignment()
        group = factory.Group(course=assignment.courses.first())
        assignment.assigned_groups.add(group)
        journal = factory.Journal(assignment=assignment)
        journal_not_viewable = factory.Journal(assignment=assignment)
        p = Participation.objects.get(user=journal.authors.first().user, course=assignment.courses.first())
        p.groups.add(group)
        assert not journal_not_viewable.authors.first().user.can_view(assignment)
        assert journal.authors.first().user.can_view(assignment)

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

    def test_update_assignment(self):
        assignment = api.create(self, 'assignments', params=self.create_params, user=self.teacher)['assignment']

        # Try to publish the assignment
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

        # Check copyable return values
        resp = api.get(self, 'assignments/copyable', user=teacher)['data']
        assert resp[0]['assignments'][0]['id'] == assignment.pk, 'copyable assignment should be displayed'
        assert len(resp[0]['assignments']) == 1
        assert resp[0]['course']['id'] == course.id, 'copyable course should be displayed'

        student = factory.Journal(assignment=assignment).authors.first().user
        data = api.get(self, 'assignments/copyable', user=student, status=200)['data']
        assert len(data) == 0, 'A student should not be able to see any copyable assignments'

        r = Participation.objects.get(course=course, user=teacher).role
        r.can_edit_assignment = False
        r.save()
        data = api.get(self, 'assignments/copyable', user=teacher)['data']
        assert len(data) == 0, 'A teacher requires can_edit_assignment to see copyable assignments.'

    def test_assignment_copy(self):
        start2018_2019 = datetime.datetime(year=2018, month=9, day=1)
        start2019_2020 = datetime.datetime(year=2019, month=9, day=1)
        end2018_2019 = start2019_2020 - relativedelta(days=1)
        end2019_2020 = datetime.datetime(year=2020, month=9, day=1) - relativedelta(days=1)

        teacher = factory.Teacher()
        course = factory.Course(
            author=teacher,
            startdate=start2018_2019,
            enddate=end2019_2020,
        )
        not_copy_course = factory.Course()
        source_assignment = factory.TemplateAssignment(
            courses=[course, not_copy_course],
            unlock_date=start2018_2019,
            due_date=end2018_2019,
            lock_date=end2018_2019,
        )
        source_assignment.active_lti_id = 'some id'
        source_assignment.save()
        source_format = source_assignment.format
        source_progress_node = factory.ProgressNode(
            format=source_format,
            unlock_date=start2018_2019,
            due_date=start2018_2019 + relativedelta(months=6),
            lock_date=start2018_2019 + relativedelta(months=6),
        )
        source_deadline_node = factory.EntrydeadlineNode(
            format=source_format,
            unlock_date=None,
            due_date=start2018_2019 + relativedelta(months=6),
            lock_date=None,
        )

        source_template = factory.Template(format=source_format)
        student = factory.Student()
        # Create student participation and accompanying journal
        factory.Participation(user=student, course=course, role=Role.objects.get(course=course, name='Student'))
        assert Participation.objects.filter(course=course).count() == 2
        source_student_journal = Journal.objects.get(authors__user=student, assignment=source_assignment)
        VLE.factory.make_journal(author=teacher, assignment=source_assignment)
        assert Journal.objects.filter(assignment=source_assignment).count() == 1, \
            'Teacher assignment should not show up in count'
        source_entries = []
        number_of_source_student_journal_entries = 4
        for _ in range(number_of_source_student_journal_entries):
            source_entries.append(factory.Entry(template=source_template, node__journal=source_student_journal))

        assert Node.objects.count() == 10, \
            '2 nodes for the presets for teacher and student each, 4 for the student entries'
        assert source_entries[0].node.journal == source_student_journal
        assert Entry.objects.filter(
            node__journal=source_student_journal).count() == number_of_source_student_journal_entries, \
            'Only the entries explicitly created above exist for the source journal'
        assert Journal.objects.filter(assignment=source_assignment).count() == 1, \
            'The source assignment only holds the journals explicitly created above'

        before_source_preset_nodes = PresetNode.objects.filter(format=source_assignment.format)
        assert source_progress_node in before_source_preset_nodes, 'We are working with the correct node and format'
        before_source_templates = Template.objects.filter(format=source_assignment.format)
        before_source_format_resp = api.get(self, 'formats', params={'pk': source_assignment.pk}, user=teacher)

        pre_copy_format_count = Format.objects.count()
        pre_copy_journal_count = Journal.all_objects.count()
        pre_copy_entry_count = Entry.objects.count()
        pre_copy_node_count = Node.objects.count()
        pre_copy_preset_node_count = PresetNode.objects.count()
        resp = api.post(self, 'assignments/{}/copy'.format(source_assignment.pk), params={
                'course_id': course.pk,
                'months_offset': 0,
            }, user=teacher)
        created_assignment = Assignment.objects.get(pk=resp['assignment_id'])
        created_format = created_assignment.format

        assert pre_copy_format_count + 1 == Format.objects.count(), 'One additional format is created'
        assert created_format == Format.objects.last(), 'Last created format should be the new assignment format'
        assert pre_copy_journal_count * 2 - 1 == Journal.all_objects.count(), \
            '''A journal should be created for each of the existing course users.
               However, old teacher should not get journal'''
        assert pre_copy_entry_count == Entry.objects.count(), 'No additional entries are created'
        assert pre_copy_node_count + 4 == Node.objects.count(), 'Both student and teacher receive nodes for the presets'
        assert pre_copy_preset_node_count + 2 == PresetNode.objects.count(), \
            'The progress and preset nodes are copied'
        assert before_source_preset_nodes.count() == PresetNode.objects.filter(
            format=created_assignment.format).count(), 'All preset nodes should be copied along.'
        assert created_assignment.active_lti_id is None, 'Copied assignment should not be linked to LTI'
        assert created_assignment.lti_id_set == [], 'Copied assignment should not be linked to LTI'
        assert created_assignment.courses.count() == 1 and course in created_assignment.courses.all(), \
            'Only the course where we call copy from should be part of the created assignment course set'

        resp = api.post(self, 'assignments/{}/copy'.format(source_assignment.pk), params={
                'course_id': course.pk,
                'months_offset': 0,
                'lti_id': 'test'
            }, user=teacher)
        created_assignment = Assignment.objects.get(pk=resp['assignment_id'])
        created_format = created_assignment.format
        assert created_assignment.author == teacher
        assert created_assignment.active_lti_id == 'test', 'Copied assignment should not be linked to LTI'
        assert created_assignment.lti_id_set == ['test'], 'Copied assignment should not be linked to LTI'

        after_source_preset_nodes = PresetNode.objects.filter(format=source_assignment.format)
        after_source_templates = Template.objects.filter(format=source_assignment.format)
        after_source_format_resp = api.get(self, 'formats', params={'pk': source_assignment.pk}, user=teacher)
        created_format_resp = api.get(self, 'formats', params={'pk': created_assignment.pk}, user=teacher)

        # Validate that the entire copied response format is unchanged
        assert before_source_format_resp == after_source_format_resp, 'Source format should remain unchanged'
        # The check above is extensive, but limited by the serializer, so let us check the db fully.
        assert before_source_preset_nodes.count() == after_source_preset_nodes.count() \
            and before_source_templates.count() == after_source_templates.count(), \
            'Format of the copy target should remain unchanged'
        for before_n, after_n in zip(before_source_preset_nodes, after_source_preset_nodes):
            assert equal_models(before_n, after_n), 'Copy target preset nodes should remain unchanged'
        for before_t, after_t in zip(before_source_templates, after_source_templates):
            assert equal_models(before_t, after_t), 'Copy target templates should remain unchanged'
        assert len(utils.get_journal_entries(source_student_journal)) == number_of_source_student_journal_entries, \
            'Old entries should not be removed'

        assert created_format.pk == created_format_resp['format']['id'], \
            'The most recently created (fresh copy) format, should be returned.'

        # Validate copy response results
        o = before_source_format_resp['format']  # original
        a = after_source_format_resp['format']
        c = created_format_resp['format']
        assert o['id'] != c['id'], 'Created format should be a new format'
        assert o['id'] == a['id'], 'Original format should be the same'
        # Validate template copy results
        for o_t, a_t, c_t in zip(o['templates'], a['templates'], c['templates']):
            assert c_t['id'] != a_t['id'], 'Should be a new template'
        # Validate preset copy results
        for o_p, a_p, c_p in zip(o['presets'], a['presets'], c['presets']):
            assert c_p['id'] != a_p['id'], 'Should be a new preset'

        # Validate the copy result values without the meddling of the serializer
        created_preset_nodes = PresetNode.objects.filter(format=created_format)
        created_templates = Template.objects.filter(format=created_format)
        assert before_source_preset_nodes.count() == created_preset_nodes.count() \
            and before_source_templates.count() == created_templates.count(), \
            'Format of the copy should be equal to the copy target'
        for before_n, created_n in zip(before_source_preset_nodes, created_preset_nodes):
            assert equal_models(before_n, created_n, ignore=['id', 'format', 'forced_template']), \
                'Copy preset nodes should be equal'
        for before_t, created_t in zip(before_source_templates, created_templates):
            assert equal_models(before_t, created_t, ignore=['id', 'format', 'forced_template']), \
                'Copy target templates should be equal'

        # Copy again, but now update all dates
        resp = api.post(self, 'assignments/{}/copy'.format(source_assignment.pk), params={
                'course_id': course.pk,
                'months_offset': 12,
            }, user=teacher)
        created_assignment = Assignment.objects.get(pk=resp['assignment_id'])
        created_format = created_assignment.format
        created_format_resp = api.get(self, 'formats', params={'pk': created_assignment.pk}, user=teacher)

        # Validate again, this time dates should be different
        c = created_format_resp['format']
        for o_p, c_p in zip(o['presets'], c['presets']):
            for key, value in c_p.items():
                if key in ['unlock_date', 'due_date', 'lock_date']:
                    if o_p[key] is None:
                        assert value is None, 'Don\'t shift deadlines that were not there to begin with.'
                    else:
                        assert relativedelta(parser.parse(value), parser.parse(o_p[key])).years == 1

        # The copy result values should still be equal apart from the dates
        created_preset_nodes = PresetNode.objects.filter(format=created_format)
        created_templates = Template.objects.filter(format=created_format)
        assert before_source_preset_nodes.count() == created_preset_nodes.count() \
            and before_source_templates.count() == created_templates.count(), \
            'Format of the copy should be equal to the copy target'
        for before_n, created_n in zip(before_source_preset_nodes, created_preset_nodes):
            assert equal_models(before_n, created_n,
                                ignore=['id', 'format', 'forced_template', 'unlock_date', 'due_date', 'lock_date']), \
                'Copy preset nodes should be equal'
        for before_t, created_t in zip(before_source_templates, created_templates):
            assert equal_models(before_t, created_t,
                                ignore=['id', 'format', 'forced_template', 'unlock_date', 'due_date', 'lock_date']), \
                'Copy target templates should be equal'

        created_progress_node = created_preset_nodes.filter(type=Node.PROGRESS).first()
        created_deadline_node = created_preset_nodes.filter(type=Node.ENTRYDEADLINE).first()
        assert created_deadline_node.unlock_date is None and created_deadline_node.lock_date is None, \
            'Times which were unset in original should not be changed'
        assert created_deadline_node.due_date.weekday() == source_deadline_node.due_date.weekday() and \
            created_progress_node.unlock_date.weekday() == source_progress_node.unlock_date.weekday() and \
            created_progress_node.due_date.weekday() == source_progress_node.due_date.weekday() and \
            created_progress_node.lock_date.weekday() == source_progress_node.lock_date.weekday() and \
            'Week days should be preserved'
        assert relativedelta(created_deadline_node.due_date, source_deadline_node.due_date).years == 1 and \
            created_deadline_node.due_date.month == source_deadline_node.due_date.month, \
            'Deadline should shift 1 year but otherwise be similar'
        assert relativedelta(created_progress_node.unlock_date, source_progress_node.unlock_date).years == 1 and \
            created_progress_node.unlock_date.month == source_progress_node.unlock_date.month, \
            'Deadline should shift 1 year but otherwise be similar'
        assert relativedelta(created_progress_node.due_date, source_progress_node.due_date).years == 1 and \
            created_progress_node.due_date.month == source_progress_node.due_date.month, \
            'Deadline should shift 1 year but otherwise be similar'
        assert relativedelta(created_progress_node.lock_date, source_progress_node.lock_date).years == 1 and \
            created_progress_node.lock_date.month == source_progress_node.lock_date.month, \
            'Deadline should shift 1 year but otherwise be similar'

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
        journal.authors.first().grade_url = 'Not None'
        journal.authors.first().sourcedid = 'Not None'
        journal.save()
        ltiAssignment1.active_lti_id = 'new lti id'
        ltiAssignment1.save()
        # Refresh the journal instance after the assignment update
        journal = Journal.objects.get(pk=journal.pk)

        assert journal.authors.first().grade_url is None and journal.authors.first().sourcedid is None, \
            'Updating the active LTI id of an assignment should reset the grade_url and sourcedid of all nested ' \
            'journals'

    def test_deadline(self):
        journal = factory.Journal(assignment=factory.TemplateAssignment())
        assignment = journal.assignment
        teacher = assignment.courses.first().author
        assignment.points_possible = 10

        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] == 'End of assignment', \
            'Default end of assignment should be shown'

        resp = api.get(self, 'assignments/upcoming', user=teacher)['upcoming']
        assert resp[0]['deadline']['date'] is None, \
            'Default no deadline for a teacher be shown'

        progress = VLE.factory.make_progress_node(assignment.format, timezone.now() + datetime.timedelta(days=3), 7)
        utils.update_journals(assignment.journal_set.distinct(), progress)

        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] == '0/7 points', \
            'When not having completed an progress node, that should be shown'

        entrydeadline = VLE.factory.make_entrydeadline_node(
            assignment.format, timezone.now() + datetime.timedelta(days=1), assignment.format.template_set.first())
        utils.update_journals(assignment.journal_set.distinct(), entrydeadline)

        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] == assignment.format.template_set.first().name, \
            'When not having completed an entry deadline, that should be shown'

        entry = factory.Entry(node=Node.objects.get(journal=journal, preset=entrydeadline))

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

        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] == '5/7 points', \
            'With only graded & published entries progres node should be the deadline'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 7, 'published': True}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] == 'End of assignment', \
            'With full points of progress node, end of assignment should be shown'

        api.create(self, 'grades', params={'entry_id': entry.pk, 'grade': 10, 'published': True}, user=teacher)
        resp = api.get(self, 'assignments/upcoming', user=journal.authors.first().user)['upcoming']
        assert resp[0]['deadline']['name'] is None, \
            'With full points of assignment, no deadline should be shown'

    def test_get_active_course(self):
        future_course = factory.Course(startdate=timezone.now() + datetime.timedelta(weeks=2))
        teacher = future_course.author
        later_future_course = factory.Course(startdate=timezone.now() + datetime.timedelta(weeks=5))
        assignment = factory.Assignment(courses=[future_course, later_future_course])
        assert assignment.get_active_course(teacher) == future_course, \
            'Select first upcomming course as there is no LTI course or course that has already started'

        past_course = factory.Course(startdate=timezone.now() - datetime.timedelta(weeks=5), author=teacher)
        assignment.courses.add(past_course)
        recent_course = factory.Course(startdate=timezone.now() - datetime.timedelta(weeks=3), author=teacher)
        assignment.courses.add(recent_course)
        assert assignment.get_active_course(teacher) == recent_course, \
            'Select most recent course as there is no LTI course'

        lti_course = factory.LtiCourseFactory(startdate=timezone.now() + datetime.timedelta(weeks=1), author=teacher)
        assignment.courses.add(lti_course)
        assignment.active_lti_id = 'lti_id'
        lti_course.assignment_lti_id_set.append('lti_id')
        lti_course.save()
        assignment.save()
        assert assignment.get_active_course(teacher) == lti_course, \
            'Select LTI course above all other courses'

        past = factory.Course(startdate=timezone.now() - datetime.timedelta(days=1))
        assignment.courses.add(past)
        future = factory.Course(startdate=timezone.now() + datetime.timedelta(days=1))
        assignment.courses.add(future)
        lti = factory.LtiCourseFactory(startdate=timezone.now() + datetime.timedelta(weeks=1))
        assignment.courses.add(lti)
        assert assignment.get_active_course(teacher) == lti_course, \
            'Do not select any course that the user is not in'
        assert assignment.get_active_course(factory.Student()) is None, \
            'When someone is not related to the assignment, it should not respond with any course'

    def test_day_neutral_datetime_increment(self):
        dt = datetime.datetime(year=2018, month=9, day=1)
        inc = day_neutral_datetime_increment(dt, 13)
        assert inc.weekday() == dt.weekday()
        assert inc.year == dt.year + 1
        assert inc.month == dt.month + 1

        inc = day_neutral_datetime_increment(dt, -13)
        assert inc.weekday() == dt.weekday()
        assert inc.year == dt.year - 1
        assert inc.month == dt.month - 1

        dt = datetime.datetime(year=2018, month=1, day=1) - relativedelta(days=1)
        inc = day_neutral_datetime_increment(dt, 1)
        assert inc.weekday() == dt.weekday()
        assert inc.year == dt.year + 1
        assert inc.month == 2, '4/2/2018 is the closest tuesday to 12/31/2017 + 1 month'

        inc = day_neutral_datetime_increment(dt, 12)
        assert inc == datetime.datetime(year=2019, month=1, day=6), \
            '06/01/2019 is the closest tuesday to 12/31/2017 + 1 year'
        assert inc.weekday() == dt.weekday()

    def test_set_assignment_dates(self):
        start2018_2019 = datetime.datetime(year=2018, month=9, day=1)
        start2019_2020 = datetime.datetime(year=2019, month=9, day=1)
        end2018_2019 = start2019_2020 - relativedelta(days=1)

        assignment = factory.Assignment(
            unlock_date=start2018_2019,
            due_date=end2018_2019,
            lock_date=end2018_2019,
        )

        set_assignment_dates(assignment, months=12)
        assert relativedelta(assignment.unlock_date, start2018_2019).years == 1 \
            and relativedelta(assignment.due_date, end2018_2019).years == 1 \
            and relativedelta(assignment.lock_date, end2018_2019).years == 1, \
            'Set dates should be moved 1 year forward'

        assignment.unlock_date = None
        assignment.due_date = None
        assignment.lock_date = None
        set_assignment_dates(assignment, months=12)
        assert assignment.unlock_date is None and assignment.due_date is None \
            and assignment.lock_date is None, \
            'Unset dates should not be modified'

    def test_create_journals(self):
        course_before = factory.Course()
        course_after = factory.Course()
        teacher = course_before.author
        student_before = factory.Student()
        student_after = factory.Student()
        normal_before = factory.Assignment(courses=[course_before])
        factory.GroupAssignment(courses=[course_before])
        normal_unpublished = factory.Assignment(courses=[course_before], is_published=False)
        factory.Participation(user=student_before, course=course_before)
        normal_after = factory.Assignment(courses=[course_before])
        group_after = factory.GroupAssignment(courses=[course_before])
        journals = Journal.all_objects.filter(authors__user=student_before)

        assert journals.filter(assignment=normal_before).exists(), 'Normal assignment should get journals'
        assert journals.filter(assignment=normal_after).exists(), \
            'Journal needs to be created even when student is added later'
        assert journals.count() == 2, 'Two journals should be created'
        journals = Journal.all_objects.filter(authors__user=teacher)
        assert journals.count() == 2, 'Teacher should also get 2 journals'

        normal_unpublished.is_group_assignment = False
        normal_unpublished.is_published = True
        normal_unpublished.save()
        journals = Journal.all_objects.filter(authors__user=student_before)
        assert journals.count() == 3, 'After publishing an extra journal needs to be created'
        journals = Journal.all_objects.filter(authors__user=teacher)
        assert journals.count() == 3, 'Teacher should also get 3 journals'

        factory.Participation(user=student_after, course=course_after)
        normal_after.add_course(course_after)
        group_after.add_course(course_after)
        journals = Journal.all_objects.filter(authors__user=student_after)
        assert journals.filter(assignment=normal_after, authors__user=student_after).exists(), \
            'Normal assignment should get journals also for students where course is added later'
        assert journals.count() == 1, 'Only normal_after should generate journal for that student'

    def test_assignment_participation_unique(self):
        journal = factory.Journal()
        student = journal.authors.first().user
        assignment = journal.assignment

        self.assertRaises(IntegrityError, AssignmentParticipation.objects.create, user=student, assignment=assignment)
