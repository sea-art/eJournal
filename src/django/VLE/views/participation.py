from rest_framework import viewsets

from VLE.models import Course, User, Role, Journal, Participation
import VLE.permissions as permissions
import VLE.utils as utils
import VLE.factory as factory
import VLE.views.responses as response
from VLE.serializers import UserSerializer
from VLE.serializers import RoleSerializer


class ParticipationView(viewsets.ViewSet):
        def list(self, request):
            """Get all users and their roles for a given course.

            Arguments:
            request -- request data
                cID -- course ID

            Returns:
            On failure:
                unauthorized -- when the user is not logged in
                keyerror -- when cID is not set as a parameter
                not found -- when the course does not exists
                forbidden -- when the user is not in the course
                forbidden -- when the user is unauthorized to view its participants
            On success:
                success -- list of all the users and their role
            """
            if not request.user.is_authenticated:
                return response.unauthorized()
            try:
                cID = request.query_params['cID']
            except KeyError:
                return response.keyerror("cID")
            try:
                course = Course.objects.get(pk=cID)
            except Course.DoesNotExist:
                return response.not_found('Course')

            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not in this course.')
            elif not role.can_view_course_participants:
                return response.forbidden('You cannot view participants in this course.')

            queryset = course.users
            role = permissions.get_role(request.user, course)
            print(role)
            # TODO: Improve how the addition of roles is done
            resp = UserSerializer(queryset, many=True).data
            for r in resp:
                r['role'] = RoleSerializer(role, many=False).data['name']
            return response.success(resp)

        def create(self, request, course_id):
            """Add a user to a course.

            Arguments:
            request -- request data
                uID -- user ID
                role -- name of the role (default: Student)
            course_id -- course ID

            Returns:
            On failure:
                unauthorized -- when the user is not logged in
                not found -- when course or user is not found
                forbidden -- when the logged in user is not connected to the course
                bad request -- when the new user is already connected to the course
                not found -- when the role doesnt exist
            On success:
                success -- success message
            """
            if not request.user.is_authenticated:
                return response.unauthorized()

            try:
                user_id = utils.required_params(request.data, 'uID')
                role_name = utils.optional_params(request.data, 'role') or 'Student'
            except KeyError:
                return response.keyerror('uID')

            try:
                user = User.objects.get(pk=user_id)
                course = Course.objects.get(pk=course_id)
            except (User.DoesNotExist, Course.DoesNotExist):
                return response.not_found('user or course')

            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not in this course.')
            elif not role.can_add_course_participants:
                return response.forbidden('You cannot add users to this course.')

            if permissions.is_user_in_course(user, course):
                return response.bad_request('User already participates in the course.')

            try:
                role = Role.objects.get(name=role_name, course=course)
            except Role.DoesNotExist:
                return response.not_found()
            factory.make_participation(user, course, role)

            assignments = course.assignment_set.all()
            role = permissions.get_role(user, course_id)
            if role.can_edit_journal:
                for assignment in assignments:
                    if not Journal.objects.filter(assignment=assignment, user=user).exists():
                        factory.make_journal(assignment, user)
            return response.success(message='Succesfully added student to course')

        def update(self, request, course_id):
            """Update user role in a course.

            Arguments:
            request -- request data
                uID -- user ID
                role -- name of the role (default: Student)
            course_id -- course ID

            Returns:
            On failure:
                unauthorized -- when the user is not logged in
                keyerror -- when the uID is not set
                not found -- when the perticipation is not found
                forbidden -- when the user is not connected to the course
                forbidden -- when the user is not allowed to change the perticipation
            On success:
                success -- with the new role name
            """
            if not request.user.is_authenticated:
                return response.unauthorized()
            try:
                user_id = utils.required_params(request.data, 'uID')
                role_name = utils.optional_params(request.data, 'role') or 'Student'
            except KeyError:
                return response.keyerror("uID")

            try:
                course = Course.objects.get(pk=course_id)
                participation = Participation.objects.get(user=user_id, course=course_id)
            except (Participation.DoesNotExist, Role.DoesNotExist, Course.DoesNotExist):
                return response.not_found('Participation, Role or Course does not exist.')

            role = permissions.get_role(request.user, course)
            if role is None:
                return response.forbidden('You are not in this course.')
            elif not role.can_edit_course_roles:
                return response.forbidden('You cannot edit the roles of this course.')

            participation.role = Role.objects.get(name=role_name, course=course_id)

            participation.save()
            return response.success(participation.role.name)
