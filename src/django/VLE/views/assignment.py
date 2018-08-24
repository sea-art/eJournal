"""
assignment.py.

In this file are all the assignment api requests.
"""
from rest_framework import viewsets
from rest_framework.decorators import action

from VLE.serializers import StudentAssignmentSerializer, TeacherAssignmentSerializer, JournalSerializer
from VLE.models import Assignment, Course, Journal
import VLE.views.responses as response
import VLE.permissions as permissions
import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.lti_grade_passback as lti_grade


class AssignmentView(viewsets.ViewSet):
    """Assignment view.

    This class creates the following api paths:
    GET /assignments/ -- gets all the assignments
    POST /assignments/ -- create a new assignment
    GET /assignments/<pk> -- gets a specific assignment
    PATCH /assignments/<pk> -- partially update an assignment
    DEL /assignments/<pk> -- delete an assignment
    GET /assignments/upcomming/ -- get the upcomming assignments of the logged in user
    PATCH /assignments/published_state/<pk> -- update the published state of an assignment of all entries in journals
    """

    def list(self, request):
        """Get the assignments from a course for the user.

        Arguments:
        request -- request data
            course_id -- course ID

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
            course_id = request.query_params['course_id']
        except KeyError:
            course_id = None
        try:
            if course_id:
                course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return response.not_found('Course')

        if course_id:
            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not in this course.')

            if role.can_grade_journal:
                queryset = course.assignment_set.all()
                serializer = TeacherAssignmentSerializer(queryset, many=True)
                resp = serializer.data
            else:
                queryset = Assignment.objects.filter(courses=course, journal__user=request.user)
                serializer = StudentAssignmentSerializer(queryset, many=True, context={'request': request})
                resp = serializer.data
        else:
            # TODO: change query to a query that selects all (upcomming) assignments connected to the user.
            serializer = StudentAssignmentSerializer(Assignment.objects.all(), context={'request': request})
            resp = serializer.data
        return response.success({'assignments': resp})

    def create(self, request):
        """Create a new assignment.

        Arguments:
        request -- request data
            name -- name of the assignment
            description -- description of the assignment
            course_id -- id of the course the assignment belongs to
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
            name, description, course_id = utils.required_params(request.data, "name", "description", "course_id")
            points_possible, lti_id = utils.optional_params(request.data, "points_possible", "lti_id")
        except KeyError:
            return response.keyerror("name", "description", "course_id")

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return response.not_found('Course')

        role = permissions.get_role(request.user, course_id)
        if role is None:
            return response.forbidden("You have no access to this course.")
        elif not role.can_add_assignment:
            return response.forbidden('You have no permissions to create an assignment.')

        assignment = factory.make_assignment(name, description, course_ids=[course_id],
                                             author=request.user, lti_id=lti_id,
                                             points_possible=points_possible)

        for user in course.users.all():
            role = permissions.get_role(user, course_id)
            if role.can_edit_journal:
                factory.make_journal(assignment, user)

        serializer = TeacherAssignmentSerializer(assignment)
        return response.created({'assignment': serializer.data})

    # TODO: Add course ID to only get the information about the assignment from that course.
    # TODO: Create a better serializer
    # TODO: split the
    def retrieve(self, request, pk=None):
        """Retrieve an assignment.

        Arguments:
        request -- request data
            lti -- if this is set, the pk is an lti_id, not a 'normal' id
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
                assignment = Assignment.objects.get(lti_id=pk)
            else:
                assignment = Assignment.objects.get(pk=pk)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        if not Assignment.objects.filter(courses__users=request.user, pk=assignment.pk):
            return response.forbidden("You cannot view this assignment.")

        role = permissions.get_assignment_permissions(request.user, assignment)
        if role['can_grade_journal']:
            serializer = TeacherAssignmentSerializer(assignment)
            journals = Journal.objects.filter(assignment=assignment)
            data = serializer.data
            data['journals'] = JournalSerializer(journals, many=True).data
        else:
            serializer = StudentAssignmentSerializer(assignment, context={'request': request})
            data = serializer.data

        return response.success({'assignment': data})

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
            course_id = int(request.query_params['course_id'])
        except KeyError:
            return response.keyerror('course_id')

        try:
            assignment = Assignment.objects.get(pk=assignment_id)
            course = Course.objects.get(pk=course_id)
        except (Assignment.DoesNotExist, Course.DoesNotExist):
            return response.not_found('course or assignment')

        # Assignments can only be deleted with can_delete_assignment permission.
        role = permissions.get_role(request.user, course)
        if not role:
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

        return response.success(data, description='Succesfully deleted the assignment.')

    @action(methods=['get'], detail=False)
    def upcomming(self, request):
        """Get upcoming deadlines for the requested user.

        Arguments:
        request -- request data
            course_id -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
        On success:
            success -- upcomming assignments

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            courses = [Course.objects.get(pk=int(request.query_params['course_id']))]
        except KeyError:
            courses = request.user.participations.all()
        except Course.DoesNotExist:
            return response.not_found('course')

        deadline_list = []

        for course in courses:
            if permissions.get_role(request.user, course):
                for assignment in Assignment.objects.filter(courses=course.id).all():
                    role = permissions.get_assignment_permissions(request.user, assignment)
                    if role['can_grade_journal']:
                        deadline_list.append(TeacherAssignmentSerializer(assignment).data)
                    else:
                        deadline_list.append(StudentAssignmentSerializer(assignment, context={'request': request}).data)

            # TODO: Specify for teacher and student seperatly, this can be done after a better serializer
            #     for assignment in Assignment.objects.filter(courses=course.id).all():
            #         deadline = create_teacher_assignment_deadline(course, assignment)
            #         if deadline:
            #             deadline_list.append(deadline)
            # else:
            #     for assignment in Assignment.objects.filter(courses=course.id, journal__user=user).all():
            #         deadline = create_student_assignment_deadline(user, course, assignment)
            #         if deadline:
            #             deadline_list.append(deadline)

        return response.success({'upcomming': deadline_list})

    @action(methods=['patch'], detail=True)
    def published_state(self, request, *args, **kwargs):
        """Update the grade publish status for whole assignment.

        Arguments:
        request -- the request that was send with
            published -- new published state
            aID -- assignment ID

        Returns a json string if it was successful or not.
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        aID = kwargs.get('pk')
        published = utils.required_params(request.data, 'published')

        try:
            assign = Assignment.objects.get(pk=aID)
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        if not permissions.has_assignment_permission(request.user, assign, 'can_publish_journal_grades'):
            return response.forbidden('You cannot publish assignments.')

        utils.publish_all_assignment_grades(assign, published)

        for journ in Journal.objects.filter(assignment=assign):
            if journ.sourcedid is not None and journ.grade_url is not None:
                payload = lti_grade.replace_result(journ)
            else:
                payload = dict()

        payload['new_published'] = published
        return response.success(payload=payload)
