"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets
from rest_framework.decorators import action

import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade
import VLE.permissions as permissions
import VLE.utils.generic_utils as utils
import VLE.views.responses as response
from VLE.models import Assignment, Course, Journal, Lti_ids
from VLE.serializers import AssignmentSerializer
from VLE.utils.error_handling import VLEMissingRequiredKey, VLEParamWrongType


class AssignmentView(viewsets.ViewSet):
    """Assignment view.

    This class creates the following api paths:
    GET /assignments/ -- gets all the assignments
    POST /assignments/ -- create a new assignment
    GET /assignments/<pk> -- gets a specific assignment
    PATCH /assignments/<pk> -- partially update an assignment
    DEL /assignments/<pk> -- delete an assignment
    GET /assignments/upcoming/ -- get the upcoming assignments of the logged in user
    """

    def list(self, request):
        """Get the assignments from a course for the user.

        Arguments:
        request -- request data
            course_id -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
        course = Course.objects.get(pk=course_id)

        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden('You are not in this course.')

        if role.can_grade:
            queryset = course.assignment_set.all()
        else:
            queryset = Assignment.objects.filter(courses=course, journal__user=request.user)
        serializer = AssignmentSerializer(queryset, many=True, context={'user': request.user, 'course': course})

        data = serializer.data
        for i, assignment in enumerate(data):
            data[i]['lti_couples'] = len(Lti_ids.objects.filter(assignment=assignment['id']))
        return response.success({'assignments': data})

    def create(self, request):
        """Create a new assignment.

        Arguments:
        request -- request data
            name -- name of the assignment
            description -- description of the assignment
            course_id -- id of the course the assignment belongs to
            points_possible -- the possible amount of points for the assignment
            unlock_date -- (optional) date the assignment becomes available on
            due_date -- (optional) date the assignment is due for
            lock_date -- (optional) date the assignment becomes unavailable on
            lti_id -- id labeled link to LTI instance

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

        name, description, course_id = utils.required_params(request.data, "name", "description", "course_id")
        points_possible, unlock_date, due_date, lock_date, lti_id, is_published = \
            utils.optional_params(request.data, "points_possible", "unlock_date", "due_date", "lock_date", "lti_id",
                                  "is_published")

        course = Course.objects.get(pk=course_id)

        role = permissions.get_role(request.user, course_id)
        if role is None:
            return response.forbidden("You have no access to this course.")
        elif not role.can_add_assignment:
            return response.forbidden('You have no permissions to create an assignment.')

        assignment = factory.make_assignment(name, description, courses=[course],
                                             author=request.user, lti_id=lti_id,
                                             points_possible=points_possible,
                                             unlock_date=unlock_date, due_date=due_date,
                                             lock_date=lock_date, is_published=is_published)

        for user in course.users.all():
            role = permissions.get_role(user, course_id)
            factory.make_journal(assignment, user)

        serializer = AssignmentSerializer(assignment, context={'user': request.user, 'course': course})
        return response.created({'assignment': serializer.data})

    def retrieve(self, request, pk=None):
        """Retrieve an assignment.

        Arguments:
        request -- request data
            lti -- if this is set, the pk is an lti_id, not a 'normal' id
            course_id -- get information about that course
        pk -- assignment ID

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

        try:
            if 'lti' in request.query_params:
                assignment = Lti_ids.objects.filter(lti_id=pk, for_model=Lti_ids.ASSIGNMENT)[0].assignment
            else:
                assignment = Assignment.objects.get(pk=pk)
        except IndexError:
            return response.not_found('Assignment does not exist.')

        try:
            course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
            course = Course.objects.get(id=course_id)
        except (VLEMissingRequiredKey, VLEParamWrongType):
            course = None

        if not Assignment.objects.filter(courses__users=request.user, pk=assignment.pk):
            return response.forbidden("You cannot view this assignment.")

        get_journals = permissions.has_assignment_permission(request.user, assignment, 'can_grade')

        serializer = AssignmentSerializer(
            assignment,
            context={'user': request.user, 'course': course, 'journals': get_journals}
        )

        return response.success({'assignment': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing assignment.

        Arguments:
        request -- request data
            data -- the new data for the assignment
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exist
            forbidden -- User not allowed to edit this assignment
            unauthorized -- when the user is unauthorized to edit the assignment
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk, = utils.required_typed_params(kwargs, (int, 'pk'))
        assignment = Assignment.objects.get(pk=pk)
        published, = utils.optional_params(request.data, 'published')
        published_response = None

        if published:
            published_response = self.publish(request, assignment)
            if published_response is False:
                return response.forbidden('You are not allowed to grade this assignment.')

        if permissions.has_assignment_permission(request.user, assignment, 'can_edit_assignment'):
            req_data = request.data
            if published is not None:
                del req_data['published']

            data = request.data

            if 'lti_id' in data:
                factory.make_lti_ids(lti_id=data['lti_id'], for_model=Lti_ids.ASSIGNMENT, assignment=assignment)

            serializer = AssignmentSerializer(assignment, data=data, context={'user': request.user}, partial=True)
            if not serializer.is_valid():
                response.bad_request()
            serializer.save()
        elif not published:
            return response.forbidden('You are not allowed to edit this assignment.')
        if published_response is not False:
            return response.success({'assignment': serializer.data, 'published': published_response})
        return response.success({'assignment': serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Delete an existing assignment from a course.

        Arguments:
        request -- request data
            course_id -- the course ID of course this assignment belongs to
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment or course does not exist
            unauthorized -- when the user is not logged in
            forbidden -- when the user cannot delete the assignment
        On success:
            success -- with a message that the course was deleted

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        assignment_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
        assignment = Assignment.objects.get(pk=assignment_id)
        course = Course.objects.get(pk=course_id)

        # Assignments can only be deleted with can_delete_assignment permission.
        role = permissions.get_role(request.user, course)
        if role is None:
            return response.forbidden(description="You have no access to this course")
        if not role.can_delete_assignment:
            return response.forbidden(description="You have no permissions to delete this assignment.")

        data = {
            'removed_completely': False,
            'removed_from_course': True
        }
        assignment.courses.remove(course)
        assignment.save()
        data['removed_from_course'] = True
        if assignment.courses.count() == 0:
            assignment.delete()
            data['removed_completely'] = True

        return response.success(data, description='Successfully deleted the assignment.')

    @action(methods=['get'], detail=False)
    def upcoming(self, request):
        """Get upcoming deadlines for the requested user.

        Arguments:
        request -- request data
            course_id -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exist
        On success:
            success -- upcoming assignments

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
            courses = [Course.objects.get(pk=course_id)]
        except (VLEMissingRequiredKey, VLEParamWrongType):
            courses = request.user.participations.all()

        deadline_list = []

        # TODO: change query to a query that selects all upcoming assignments connected to the user.
        for course in courses:
            if permissions.get_role(request.user, course):
                for assignment in Assignment.objects.filter(courses=course.id, is_published=True).all():
                    deadline_list.append(
                        AssignmentSerializer(assignment, context={'user': request.user, 'course': course}).data)

        return response.success({'upcoming': deadline_list})

    @action(methods=['patch'], detail=True)
    def published_state(self, request, *args, **kwargs):
        """Update the grade publish status for whole assignment.

        Arguments:
        request -- the request that was send with
            published -- new published state
            assignment_id -- assignment ID

        Returns a json string if it was successful or not.
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        assignment_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        published, = utils.required_params(request.data, 'published')
        assign = Assignment.objects.get(pk=assignment_id)

        if not permissions.has_assignment_permission(request.user, assign, 'can_publish_grades'):
            return response.forbidden('You are not allowed to publish grades for this assignment.')

        utils.publish_all_assignment_grades(assign, published)

        for journ in Journal.objects.filter(assignment=assign):
            if journ.sourcedid is not None and journ.grade_url is not None:
                lti_grade.replace_result(journ)

        return response.success(payload={'new_published': published})

    def publish(self, request, assignment, published=True):
        if permissions.has_assignment_permission(request.user, assignment, 'can_publish_grades'):
            utils.publish_all_assignment_grades(assignment, published)

            for journal in Journal.objects.filter(assignment=assignment):
                if journal.sourcedid is not None and journal.grade_url is not None:
                    payload = lti_grade.replace_result(journal)
                else:
                    payload = dict()

            return payload
        else:
            return False
