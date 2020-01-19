"""
journal.py.

In this file are all the journal api requests.
"""
from rest_framework import viewsets
from rest_framework.decorators import action

import VLE.lti_grade_passback as lti_grade
import VLE.tasks.lti as lti_tasks
import VLE.utils.generic_utils as utils
import VLE.utils.grading as grading
import VLE.utils.responses as response
from VLE.models import Assignment, AssignmentParticipation, Course, Entry, Journal, User
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

        if assignment.is_group_assignment:
            queryset = assignment.journal_set
        else:
            users = course.participation_set.filter(role__can_have_journal=True).values('user')
            queryset = assignment.journal_set.filter(authors__user__in=users)
        journals = JournalSerializer(
            queryset.distinct().order_by('pk'),
            many=True,
            context={
                'user': request.user,
                'course': course,
            }).data

        return response.success({'journals': journals})

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

    def create(self, request):
        """Create a batch of journals.

        Arguments:
        request -- request data
            amount -- amount of journals to create
            author_limit -- maximum amount of users in journal
            assignment_id -- assignment to create the journals in
            name -- (optional) name of the journal (default 'Journal')
        """
        amount, author_limit, assignment_id = utils.required_typed_params(
            request.data, (int, 'amount'), (int, 'author_limit'), (int, 'assignment_id'))
        name, = utils.optional_params(request.data, 'name')
        if name is None:
            name = 'Journal'
        assignment = Assignment.objects.get(pk=assignment_id)
        if amount < 1:
            return response.bad_request('Number of journals needs to be higher than 0.')

        request.user.check_permission('can_manage_journals', assignment)

        journals = []
        for i in range(amount):

            journals.append(Journal.objects.create(
                assignment=assignment,
                author_limit=author_limit,
                name=self._get_name(name, amount, assignment)
            ))

        serializer = JournalSerializer(
            Journal.objects.filter(assignment=assignment), many=True, context={'user': request.user})
        return response.created({'journals': serializer.data})

    def _get_name(self, name, amount, assignment):
        # Get other journal names with the same name
        journal_names = Journal.objects.filter(
            assignment=assignment,
            name__regex=r"^({0} [\d]*)$|(^{0}$)".format(name)
        ).values_list('name', flat=True)

        # If there are no other journals like it, just set the name as is
        if amount == 1 and not journal_names:
            return name

        # If "Journal" exists, the second one needs to be "Journal 2", not "Journal 1"
        extra = 2 if Journal.objects.filter(name=name).exists() else 1
        # Find the first empty spot for the journal name
        while True:
            if '{} {}'.format(name, extra) not in journal_names:
                return '{} {}'.format(name, extra)
            extra += 1

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

        request.user.check_can_view(journal)

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

        name, author_limit, image = utils.optional_typed_params(request.data, (str, 'name'), (int, 'author_limit'),
                                                                (str, 'image'))
        if name is not None or author_limit is not None or image is not None:
            # Update name if allowed
            if name is not None:
                if not request.user.has_permission('can_manage_journals', journal.assignment):
                    if not journal.assignment.can_set_journal_name:
                        return response.forbidden('You are not allowed to change the journal name.')
                journal.name = name
                journal.save()
            # Update image if allowed
            if image is not None:
                if not request.user.has_permission('can_manage_journals', journal.assignment):
                    if not journal.assignment.can_set_journal_image:
                        return response.forbidden('You are not allowed to change the journal image.')
                journal.image = image
                journal.save()
            # Update author_limit if allowed
            if author_limit is not None:
                if not request.user.has_permission('can_manage_journals', journal.assignment):
                    return response.forbidden('You are not allowed to change the max users.')
                if not journal.assignment.is_group_assignment:
                    return response.bad_request('You can only set author_limit for group assignments.')
                if author_limit != 0 and journal.authors.count() > author_limit:
                    return response.bad_request('There are too many student in this journal.')
                journal.author_limit = author_limit
                journal.save()
            return response.success({'journal': JournalSerializer(journal, context={'user': request.user}).data})

        if request.user.is_superuser:
            return self.admin_update(request, journal)

        return response.bad_request('No valid values were specified.')

    def destroy(self, request, *args, **kwargs):
        """Deleting a journals"""
        journal_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        journal = Journal.objects.get(pk=journal_id)

        request.user.check_can_view(journal.assignment)
        request.user.check_permission('can_manage_journals', journal.assignment)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('Only journals from a group assignment can be deleted.')

        if journal.authors.exists():
            return response.bad_request('There are still authors in this journal.')

        journal.delete()
        return response.success(description='Successfully deleted the journal.')

    @action(['patch'], detail=True)
    def join(self, request, pk):
        """Become a member of a journal"""
        journal = Journal.objects.get(pk=pk)
        # TODO GROUPS: result data needs to be set to LTI passback when student joins.
        # Only when entries need to be graded
        # Check if user can have journal in assignment
        request.user.check_can_view(journal.assignment)
        request.user.check_permission('can_have_journal', journal.assignment)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('Joining journals is only allowed for group assignments.')
        if journal.locked:
            return response.bad_request('You are not allowed to join a locked journal.')

        # Check if it is valid to join journal
        if journal.authors.filter(user=request.user).exists():
            return response.bad_request('You are already in this journal.')
        if Journal.objects.filter(assignment=journal.assignment, authors__user=request.user).exists():
            return response.bad_request('You may only be in one journal at the time.')
        if journal.author_limit != Journal.UNLIMITED and journal.authors.count() >= journal.author_limit:
            return response.bad_request('This journal is already full.')

        author = AssignmentParticipation.objects.get(assignment=journal.assignment, user=request.user)
        journal.authors.add(author)
        lti_tasks.join_journal_passback.delay(author.pk, journal.pk)

        serializer = JournalSerializer(journal, context={'user': request.user})
        return response.success({'journal': serializer.data})

    @action(['patch'], detail=True)
    def add_members(self, request, pk):
        """Add a member to the journal.

        Arguments:
        request -- request data
            user_id -- user who joins the journal
        """
        journal = Journal.objects.get(pk=pk)

        request.user.check_permission('can_edit_assignment', journal.assignment)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('Joining journals is only allowed for group assignments.')

        user_ids, = utils.required_typed_params(request.data, (int, 'user_ids'))

        if journal.author_limit != Journal.UNLIMITED and \
                journal.authors.count() + len(user_ids) > journal.author_limit:
            return response.bad_request('Adding these members would exceed this journal\'s member limit.')

        users = User.objects.filter(pk__in=user_ids)

        for user in users:
            # Check if users can have journal in assignment
            user.check_participation(journal.assignment)
            user.check_permission('can_have_journal', journal.assignment)

            # Check if it is valid to join journal
            if journal.authors.filter(user=user).exists():
                return response.bad_request('{} is already a member of this journal.'.format(user.full_name))
            if Journal.objects.filter(assignment=journal.assignment, authors__user=user).exists():
                return response.bad_request('{} is already a member of another journal.'.format(user.full_name))

        for user in users:
            author = AssignmentParticipation.objects.get(assignment=journal.assignment, user=user)
            journal.authors.add(author)
            lti_tasks.join_journal_passback.delay(author.pk, journal.pk)

        serializer = JournalSerializer(journal, context={'user': request.user})
        return response.success({'journal': serializer.data})

    @action(['patch'], detail=True)
    def leave(self, request, pk):
        """Leave a journal"""
        journal = Journal.objects.get(pk=pk)
        # TODO GROUPS: result data needs to be reset on LTI passback when student leaves
        # Links needs to be set to where the teacher gets explained that the author recently left
        request.user.check_can_view(journal.assignment)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only leave group assignments.')

        if not journal.authors.filter(user=request.user).exists():
            return response.bad_request('You are currently not a member of this journal.')

        if journal.locked:
            return response.bad_request('You are not allowed to leave a locked journal.')

        author = AssignmentParticipation.objects.get(user=request.user, journal=journal)
        journal.authors.remove(author)
        if journal.authors.count() == 0:
            journal.reset()

        lti_tasks.left_journal_passback.delay(author.pk, journal.pk)
        return response.success(description='Successfully removed from the journal.')

    @action(['patch'], detail=True)
    def kick(self, request, pk):
        """Kick a student from the journal

        Arguments:
        request -- request data
            user_id -- user of student who gets kicked from the journal
        """
        journal = Journal.objects.get(pk=pk)

        request.user.check_permission('can_edit_assignment', journal.assignment)

        user_id, = utils.required_typed_params(request.data, (int, 'user_id'))
        user = User.objects.get(pk=user_id)

        if not journal.assignment.is_group_assignment:
            return response.bad_request('Students can only be kicked from journals in group assignments.')

        if not journal.authors.filter(user=user).exists():
            return response.bad_request('Student is currently not a member of this journal.')

        author = AssignmentParticipation.objects.get(user=user, journal=journal)
        journal.authors.remove(author)
        if journal.authors.count() == 0:
            journal.reset()

        lti_tasks.left_journal_passback.delay(author.pk, journal.pk)

        return response.success(description='Successfully removed {} from the journal.'.format(author.user.full_name))

    @action(['patch'], detail=True)
    def lock(self, request, pk):
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal.assignment)

        if not request.user.has_permission('can_manage_journals', journal.assignment):
            if not journal.authors.filter(user=request.user).exists():
                return response.bad_request('You can only lock members of journals that you are a member of yourself.')
            elif not journal.assignment.can_lock_journal:
                return response.bad_request('The teacher disabled (un)locking journal members for students.')

        if not journal.assignment.is_group_assignment:
            return response.bad_request('You can only lock journal members for group assignments.')

        journal.locked, = utils.required_typed_params(request.data, (bool, 'locked'))
        journal.save()

        return response.success(description='Successfully {}locked journal members.'.format(
            '' if journal.locked else 'un'))

    def admin_update(self, request, journal):
        req_data = request.data
        if 'published' in req_data:
            del req_data['published']
        serializer = JournalSerializer(journal, data=req_data, partial=True, context={'user': request.user})
        if not serializer.is_valid():
            return response.bad_request()
        serializer.save()

        return response.success({'journal': serializer.data})

    def publish(self, request, journal):
        grading.publish_all_journal_grades(journal, request.user)
        if journal.authors.filter(sourcedid__isnull=False).exists():
            payload = lti_grade.replace_result(journal)
            if payload and 'code_mayor' in payload and payload['code_mayor'] == 'success':
                return response.success({
                    'journal': JournalSerializer(journal, context={'user': request.user}).data
                })
            else:
                return response.bad_request({
                    'journal': JournalSerializer(journal, context={'user': request.user}).data
                })
        else:
            return response.success({
                'journal': JournalSerializer(journal, context={'user': request.user}).data
            })
