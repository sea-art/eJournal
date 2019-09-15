"""
assignment.py.

In this file are all the assignment api requests.
"""
from django.db.models import Q
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action

import VLE.factory as factory
import VLE.lti_grade_passback as lti_grade
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
import VLE.validators as validators
from VLE.models import Assignment, Course, Journal, User
from VLE.serializers import AssignmentDetailsSerializer, AssignmentSerializer, CourseSerializer
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
        On success:
            success -- with the assignment data

        """
        try:
            course_id, = utils.optional_typed_params(request.query_params, (int, 'course_id'))
            course = Course.objects.get(pk=course_id)
            request.user.check_participation(course)
            courses = [course]
        except VLEParamWrongType:
            course = None
            courses = request.user.participations.all()

        query = Assignment.objects.filter(courses__in=courses).distinct()
        viewable = [assignment for assignment in query if request.user.can_view(assignment)]
        serializer = AssignmentSerializer(viewable, many=True, context={'user': request.user, 'course': course})

        data = serializer.data
        for i, assignment in enumerate(data):
            data[i]['lti_couples'] = len(Assignment.objects.get(id=assignment['id']).lti_id_set)
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
            lti_id -- (optional) id labeled link to LTI instance

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            key_error -- missing keys
            forbidden -- the user is not allowed to create assignments in this course

        On success:
            success -- with the assignment data

        """
        name, description, course_id = utils.required_params(request.data, "name", "description", "course_id")
        points_possible, unlock_date, due_date, lock_date, active_lti_id, is_published = \
            utils.optional_params(request.data, "points_possible", "unlock_date", "due_date", "lock_date", "lti_id",
                                  "is_published")
        course = Course.objects.get(pk=course_id)

        request.user.check_permission('can_add_assignment', course)

        assignment = factory.make_assignment(name, description, courses=[course],
                                             author=request.user, active_lti_id=active_lti_id,
                                             points_possible=points_possible,
                                             unlock_date=unlock_date, due_date=due_date,
                                             lock_date=lock_date, is_published=is_published)

        if active_lti_id is not None:
            course.set_assignment_lti_id_set(active_lti_id)
            course.save()

        for user in course.users.all():
            factory.make_journal(assignment, user)

        serializer = AssignmentSerializer(
            assignment,
            context={'user': request.user, 'course': course,
                     'journals': request.user.has_permission('can_grade', assignment)}
        )
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
            success -- with the assignment data

        """
        if 'lti' in request.query_params:
            assignment = Assignment.objects.get(lti_id_set__contains=[pk])
        else:
            assignment = Assignment.objects.get(pk=pk)

        try:
            course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
            course = Course.objects.get(id=course_id)
        except (VLEMissingRequiredKey, VLEParamWrongType):
            course = None

        request.user.check_can_view(assignment)

        serializer = AssignmentSerializer(
            assignment,
            context={'user': request.user, 'course': course,
                     'journals': request.user.has_permission('can_grade', assignment)}
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
        pk, = utils.required_typed_params(kwargs, (int, 'pk'))
        assignment = Assignment.objects.get(pk=pk)

        request.user.check_permission('can_edit_assignment', assignment)

        response_data = {}

        # Remove data that must not be changed by the serializer
        req_data = request.data
        if not (request.user.is_superuser or request.user == assignment.author):
            req_data.pop('author', None)

        # Check if the assignment can be unpublished
        is_published, = utils.optional_params(request.data, 'is_published')
        if not assignment.can_unpublish() and is_published is False:
            return response.bad_request('You cannot unpublish an assignment that already has submissions.')

        active_lti_course, = utils.optional_typed_params(request.data, (int, 'active_lti_course'))
        if active_lti_course is not None:
            course = Course.objects.get(pk=active_lti_course)
            active_lti_id = assignment.get_course_lti_id(course)
            if active_lti_id:
                assignment.active_lti_id = active_lti_id
                assignment.save()

        # Rename lti id key for serializer
        if 'lti_id' in req_data:
            course_id, = utils.required_params(request.data, 'course_id')
            course = Course.objects.get(pk=course_id)
            request.user.check_permission('can_add_assignment', course)
            if course in assignment.courses.all():
                return response.bad_request('Assignment already used in course.')
            course.set_assignment_lti_id_set(req_data['lti_id'])
            course.save()
            assignment.courses.add(course)
            assignment.save()
            for user in User.objects.filter(participation__course=course).exclude(journal__assignment=assignment):
                factory.make_journal(assignment, user)
            req_data['active_lti_id'] = req_data.pop('lti_id')

        # Update the other data
        serializer = AssignmentSerializer(assignment, data=req_data, context={'user': request.user}, partial=True)
        if not serializer.is_valid():
            return response.bad_request()
        serializer.save()
        response_data['assignment'] = serializer.data

        return response.success(response_data)

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
        assignment_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
        assignment = Assignment.objects.get(pk=assignment_id)
        course = Course.objects.get(pk=course_id)

        request.user.check_permission('can_delete_assignment', course)

        intersecting_assignment_lti_id = assignment.get_course_lti_id(course)
        if intersecting_assignment_lti_id:
            if assignment.active_lti_id == intersecting_assignment_lti_id and len(assignment.lti_id_set) > 1:
                return response.bad_request('This assignment cannot be removed from this course, since it is' +
                                            ' currently configured for grade passback to the LMS')
            course.assignment_lti_id_set.remove(intersecting_assignment_lti_id)
            assignment.lti_id_set.remove(intersecting_assignment_lti_id)
            course.save()

        assignment.courses.remove(course)
        assignment.save()

        if assignment.active_lti_id is not None and assignment.active_lti_id in course.assignment_lti_id_set:
            course.assignment_lti_id_set.remove(assignment.active_lti_id)
            course.save()

        # If the assignment is only connected to one course, delete it completely
        if assignment.courses.count() == 0:
            assignment.delete()
            return response.success(description='Successfully deleted the assignment.')
        else:
            return response.success(description='Successfully removed the assignment from {}.'.format(str(course)))

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
        try:
            course_id, = utils.required_typed_params(request.query_params, (int, 'course_id'))
            course = Course.objects.get(pk=course_id)
            courses = [course]
        except (VLEMissingRequiredKey, VLEParamWrongType):
            course = None
            courses = request.user.participations.all()

        now = timezone.now()
        query = Assignment.objects.filter(
            Q(lock_date__gt=now) | Q(lock_date=None), courses__in=courses
        ).distinct()
        viewable = [assignment for assignment in query if request.user.can_view(assignment)]
        upcoming = AssignmentSerializer(viewable, context={'user': request.user, 'course': course}, many=True).data

        return response.success({'upcoming': upcoming})

    @action(methods=['post'], detail=True)
    def add_bonus_points(self, request, *args, **kwargs):
        """Give students bonus points though file submission.

        This will scan over the included file, and give all the users the bonus points supplied.
        Format:
        [username1], [bonus_points1]
        [username2], [bonus_points2]

        Arguments:
        request
            file -- list of all the bonus points
        pk -- assignment ID
        """
        assignment_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        assignment = Assignment.objects.get(pk=assignment_id)

        request.user.check_permission('can_grade', assignment)

        if not (request.FILES and 'file' in request.FILES):
            return response.bad_request('No accompanying file found in the request.')

        validators.validate_user_file(request.FILES['file'], request.user)

        bonuses = dict()
        incorrect_format_lines = dict()
        unknown_users = dict()
        duplicates = dict()
        non_participants = dict()

        for line_nr, line in enumerate(request.FILES['file'], 1):
            try:
                decoded_line = line.decode()

                # Ignore empty lines.
                if not decoded_line.strip():
                    continue

                username, bonus = decoded_line[:-1].split(',')[:2]
                bonus = float(bonus)
                user = User.objects.get(username=str(username))
                journal = Journal.objects.get(assignment=assignment, user=user)
                if journal in bonuses:
                    duplicates[line_nr] = line.decode().split(',')[0]
                else:
                    bonuses[journal] = bonus
            except UnicodeDecodeError:
                return response.bad_request({'general': 'Not a valid csv file.'})
            except ValueError:
                incorrect_format_lines[line_nr] = line.decode()
            except User.DoesNotExist:
                unknown_users[line_nr] = line.decode().split(',')[0]
            except Journal.DoesNotExist:
                non_participants[line_nr] = line.decode().split(',')[0]

        if unknown_users or incorrect_format_lines or duplicates:
            errors = dict()

            if incorrect_format_lines:
                errors['incorrect_format_lines'] = incorrect_format_lines
            if duplicates:
                errors['duplicates'] = duplicates
            if unknown_users:
                errors['unknown_users'] = unknown_users
            if non_participants:
                errors['non_participants'] = non_participants

            return response.bad_request(errors)

        for j, b in bonuses.items():
            j.bonus_points = b
            j.save()
            lti_grade.replace_result(journal)

        return response.success()

    @action(methods=['get'], detail=True)
    def copyable(self, request, pk):
        """Get all assignments that a user can copy a format from, except for the current assignment.

        Arguments:
        pk -- assignment ID

        Returns a list of tuples consisting of courses and copyable assignments."""
        courses = Course.objects.filter(participation__user=request.user.id,
                                        participation__role__can_edit_assignment=True)

        copyable = []
        for course in courses:
            assignments = Assignment.objects.filter(courses=course).exclude(pk=pk)
            if assignments:
                copyable.append({
                    'course': CourseSerializer(course).data,
                    'assignments': AssignmentDetailsSerializer(assignments, context={'user': request.user},
                                                               many=True).data
                })
        return response.success({'data': copyable})
