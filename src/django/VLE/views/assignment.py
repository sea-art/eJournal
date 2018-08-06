"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets

from VLE.serializers import StudentAssignmentSerializer, TeacherAssignmentSerializer, JournalSerializer, UserSerializer
from VLE.models import Assignment, Course, Journal
import VLE.views.responses as response
import VLE.permissions as permissions
import VLE.factory as factory
import VLE.utils as utils


class AssignmentView(viewsets.ViewSet):
    serializer_class = StudentAssignmentSerializer

    def list(self, request):
        """Get the assignments from a course for the user.

        Arguments:
        request -- request data
            cID -- the ID of the course

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the assignment data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()
        try:
            cID = request.query_params['cID']
        except KeyError:
            cID = None
        try:
            if cID:
                course = Course.objects.get(pk=cID)
        except Course.DoesNotExist:
            return response.not_found('Course')

        if cID:
            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not in this course.')

            if not role.can_grade_journal:
                queryset = course.assignment_set.all()
                serializer = StudentAssignmentSerializer(queryset, many=True)
            else:
                queryset = Assignment.objects.filter(courses=course, journal__user=request.user)
                serializer = TeacherAssignmentSerializer(queryset, many=True)
        else:
            # TODO: change query to a query that selects all (upcomming) assignments connected to the user.
            serializer = StudentAssignmentSerializer(Assignment.objects.all())

        return response.success(serializer.data)

    def create(self, request):
        """Create a new assignment.

        Arguments:
        request -- the request that was send with
            name -- name of the assignment
            description -- description of the assignment
            cID -- id of the course the assignment belongs to
            points_possible -- the possible amount of points for the assignment

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            key_error -- missing keys
            forbidden -- the user is not allowed to create assignments in this course

        On success:
            succes -- with the assignment data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            name, description, cID = utils.required_params(request.data, "name", "description", "cID")
            points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
        except KeyError:
            return response.keyerror("name", "description", "cID")

        try:
            Course.objects.get(pk=cID)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, cID)

        if role is None:
            return response.forbidden("You have no access to this course.")
        elif not role.can_add_assignment:
            return response.forbidden('You have no permissions to create an assignment.')

        assignment = factory.make_assignment(name, description, cIDs=[cID],
                                             author=request.user, lti_id=lti_id,
                                             points_possible=points_possible)

        serializer = TeacherAssignmentSerializer(assignment)
        return response.created(serializer.data, obj='assignment')

    # TODO: Add course ID to only get the information about the assignment from that course.
    def retrieve(self, request, pk=None):
        """Retrieve an assignment.

        Arguments:
        request -- the request that was send with
        pk -- the assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            forbidden -- not allowed to retrieve assignments in this course

        On success:
            succes -- with the assignment data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if pk is None:
            return response.bad_request('pk is missing')

        try:
            assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        if not Assignment.objects.filter(courses__users=request.user, pk=pk):
            return response.forbidden("You cannot view this assignment.")

        serializer = self.serializer_class(assignment)
        data = serializer.data
        journals = Journal.objects.filter(assignment=assignment)
        data['journals'] = JournalSerializer(journals, many=True).data
        for i, journal in enumerate(journals):
            entries = utils.get_journal_entries(journal)
            data['journals'][i]['stats'] = {
                'acquired_points': utils.get_acquired_points(entries),
                'graded': utils.get_graded_count(entries),
                'submitted': utils.get_submitted_count(entries),
                'total_points': utils.get_max_points(journal),
            }
            try:
                data['journals'][i]['student'] = UserSerializer(journal.user).data
            except Journal.DoesNotExist:
                continue
        return response.success(data)

    def update(self, request, *args, **kwargs):
        pass

    def partial_update(self, request, *args, **kwargs):
        """Update an existing assignment.

        Arguments:
        request -- request data
            data -- the new data for the course
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exists
            forbidden -- User not allowed to edit this assignment
            unauthorized -- when the user is unauthorized to edit the assignment
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new assignment data
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk = kwargs.get('pk')

        try:
            assignment = Assignment.objects.get(pk=pk)
        except Course.DoesNotExist:
            return response.not_found('Assignment')

        if not permissions.has_assignment_permission(request.user, assignment, 'can_edit_assignment'):
            return response.forbidden('You are not allowed to edit this assignment.')

        serializer = TeacherAssignmentSerializer(assignment, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()
        return response.success(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Delete an existing assignment from a course.

        Arguments:
        request -- request data
        pk -- assignment ID

        Returns:
        On failure:
            not found -- when the assignment or course does not exists
            unauthorized -- when the user is not logged in
            forbidden -- when the user cannot delete the assignment
        On success:
            success -- with a message that the course was deleted
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        assignment_id = kwargs.get('pk')

        try:
            course_id = int(request.query_params['cID'])
        except KeyError:
            return response.keyerror('cID')

        try:
            assignment = Assignment.objects.get(pk=assignment_id)
            course = Course.objects.get(pk=course_id)
        except (Assignment.DoesNotExist, Course.DoesNotExist):
            return response.not_found('course or ssignment')

        # Assignments can only be deleted with can_delete_assignment permission.
        role = permissions.get_role(request.user, course)
        if not role:
            return response.forbidden(description="You have no access to this course")
        if not role.can_delete_assignment:
            return response.forbidden(description="You have no permissions to delete this assignment.")

        data = {'removed_completely': False}
        assignment.courses.remove(course)
        assignment.save()
        data['removed_from_course'] = True
        if assignment.courses.count() == 0:
            assignment.delete()
            data['removed_completely'] = True

        return response.success(data, description='Removed assignment')
