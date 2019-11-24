"""
journal.py.

In this file are all the journal api requests.
"""
from rest_framework import viewsets
from rest_framework.decorators import action

import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade
import VLE.utils.generic_utils as utils
import VLE.utils.grading as grading
import VLE.utils.responses as response
from VLE.models import Assignment, AssignmentParticipation, Course, Journal
from VLE.serializers import JournalSerializer


class JournalView(viewsets.ViewSet):
    """Journal view.

    This class creates the following api paths:
    GET /journals/ -- gets all the journals
    GET /journals/<pk> -- gets a specific journal
    POST /journals/ -- create a new journal
    PATCH /journals/<pk> -- partially update an journal
    DEL /journals/<pk> -- delete an journal
    """

    def list(self, request):
        """Get the student submitted journals of one assignment from a course.

        Arguments:
        request -- request data
            course_id -- course ID
            assignment_id -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exist
            forbidden -- when the user has no permission to view the journals of the assignment
        On success:
            success -- with journals and stats about the journals

        """
        assignment_id, course_id = utils.required_typed_params(request.query_params,
                                                               (int, 'assignment_id'), (int, 'course_id'))
        assignment = Assignment.objects.get(pk=assignment_id)
        course = Course.objects.get(pk=course_id)

        request.user.check_can_view(assignment)
        if not assignment.is_group_assignment:
            request.user.check_permission('can_view_all_journals', assignment)

        users = course.participation_set.filter(role__can_have_journal=True).values('user')
        queryset = assignment.journal_set.order_by('pk')
        journals = JournalSerializer(
            queryset,
            many=True,
            context={
                'user': request.user,
                'course': course,
            }).data

        return response.success({'journals': journals})

    def create(self, request):
        """Create a journal.

        This is used for group assignments when the student needs to create their own journal.
        """
        assignment_id, = utils.required_typed_params(request.data, (int, "assignment_id"))
        assignment = Assignment.objects.get(pk=assignment_id)

        request.user.check_can_view(assignment)
        if Journal.objects.filter(assignment=assignment, authors__user=request.user).exists():
            return response.bad_request('You may only be in one journal at the time.')

        journal = factory.make_journal(assignment, request.user)
        serializer = JournalSerializer(journal, context={'user': request.user, 'course': course})
        return response.created({'journal': serializer.data})

    def retrieve(self, request, pk):
        """Get a student submitted journal.

        Arguments:
        request -- request data
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exist
            forbidden -- when the user has no permission to view the journal
        On success:
            success -- with journals and stats about the journals

        """
        journal = Journal.objects.get(pk=pk)
        request.user.check_can_view(journal)

        serializer = JournalSerializer(journal, context={
            'user': request.user,
        })
        return response.success({'journal': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing journal.

        Arguments:
        request -- request data
            data -- the new data for the journal
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exist
            forbidden -- User not allowed to edit this journal
            unauthorized -- when the user is unauthorized to edit the journal
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new journal data

        """
        pk, = utils.required_typed_params(kwargs, (int, 'pk'))
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal.assignment)

        req_data = request.data
        published, = utils.optional_params(request.data, 'published')
        if published:
            request.user.check_permission('can_publish_grades', journal.assignment)
            req_data.pop('published', None)
            return self.publish(request, journal)

        bonus_points, = utils.optional_typed_params(request.data, (float, 'bonus_points'))
        if bonus_points is not None:
            request.user.check_permission('can_grade', journal.assignment)
            req_data.pop('bonus_points', None)
            journal.bonus_points = bonus_points
            journal.save()
            lti_grade.replace_result(journal)
            return response.success({'journal': JournalSerializer(journal, context={'user': request.user}).data})

        if not request.user.is_superuser:
            return response.forbidden('You are not allowed to edit this journal.')

        return self.admin_update(request, journal)

    @action(['patch'], detail=True)
    def join(self, request, pk):
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal.assignment)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only join group assignments.')

        if journal.locked:
            return response.bad_request('You are not allowed to join a locked journal.')

        if journal.authors.count() >= journal.max_users:
            return response.bad_request('This journal is already full.')

        if Journal.objects.filter(assignment=journal.assignment, authors__user=request.user).exists():
            return response.bad_request('You may only be in one journal at the time.')

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only join group assignments.')

        if request.user.has_permission('can_view_all_journals', journal.assignment):
            return response.bad_request('You are not allowed to join a journal as a teacher.')

        student = AssignmentParticipation.objects.get(assignment=journal.assignment, user=request.user)
        journal.authors.add(student)
        journal.save()

        serializer = JournalSerializer(journal, context={'user': request.user})
        return response.success({'journal': serializer.data})

    @action(['patch'], detail=True)
    def leave(self, request, pk):
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal.assignment)

        if not journal.authors.filter(user=request.user).exists():
            return response.bad_request('You are currently not in this journal.')

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only leave group assignments.')

        if journal.locked:
            return response.bad_request('You are not allowed to leave a locked journal.')

        author = AssignmentParticipation.objects.get(user=request.user, journal=journal)
        journal.authors.remove(author)
        journal.save()

        return response.success(description='Successfully removed from the journal.')

    @action(['patch'], detail=True)
    def lock(self, request, pk):
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal.assignment)

        if not request.user.has_permission('can_edit_assignment', journal.assignment):
            if not journal.authors.filter(user=request.user).exists():
                return response.bad_request('You can only lock journals that you are in.')
            elif not journal.assignment.can_lock_journal:
                return response.bad_request('The teacher has disabled (un)locking journals.')

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only lock group assignments.')

        journal.locked, = utils.required_typed_params(request.data, (bool, 'locked'))
        journal.save()

        return response.success(description='Successfully {}locked the journal.'.format('' if journal.locked else 'un'))

    def admin_update(self, request, journal):
        req_data = request.data
        if 'published' in req_data:
            del req_data['published']
        serializer = JournalSerializer(journal, data=req_data, partial=True, context={'user': request.user})
        if not serializer.is_valid():
            return response.bad_request()
        serializer.save()

        return response.success({'journal': serializer.data})

    # TODO: lti_info is never used, move replace_result to celery
    def publish(self, request, journal):
        grading.publish_all_journal_grades(journal, request.user)
        if journal.authors.filter(sourcedid__isnull=False).exists():
            payload = lti_grade.replace_result(journal)
            if payload and 'code_mayor' in payload and payload['code_mayor'] == 'success':
                return response.success({
                    'lti_info': payload,
                    'journal': JournalSerializer(journal, context={'user': request.user}).data
                })
            else:
                return response.bad_request({
                    'lti_info': payload,
                    'journal': JournalSerializer(journal, context={'user': request.user}).data
                })
        else:
            return response.success({
                'journal': JournalSerializer(journal, context={'user': request.user}).data
            })
