"""
Serializers.

Functions to convert certain data to other formats.
"""
from django.db.models import Min, Q
from django.utils import timezone
from rest_framework import serializers

import VLE.permissions as permissions
from VLE.models import (Assignment, Comment, Content, Course, Entry, Field, Format, Grade, Group, Instance, Journal,
                        Node, Participation, Preferences, PresetNode, Role, Template, User)
from VLE.utils import generic_utils as utils
from VLE.utils.error_handling import VLEParticipationError, VLEProgrammingError


class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instance
        fields = ('allow_standalone_registration', 'name')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'full_name', 'profile_picture', 'is_teacher', 'lti_id', 'id',
                  'role', 'groups')
        read_only_fields = ('id', 'lti_id', 'is_teacher', 'username')

    def get_role(self, user):
        if 'course' not in self.context or not self.context['course']:
            return None

        role = Participation.objects.get(user=user, course=self.context['course']).role

        if role:
            return role.name
        else:
            return None

    def get_groups(self, user):
        if 'course' not in self.context or not self.context['course']:
            return None
        try:
            groups = Participation.objects.get(user=user, course=self.context['course']).groups
            return GroupSerializer(groups, many=True, context=self.context).data
        except Participation.DoesNotExist:
            return None


class OwnUserSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'permissions', 'is_superuser',
                  'lti_id', 'profile_picture', 'is_teacher', 'verified_email')
        read_only_fields = ('id', 'permissions', 'lti_id', 'is_teacher', 'verified_email', 'username', 'is_superuser')

    def get_permissions(self, user):
        """Returns a dictionary with all user permissions.

        Arguments:
        user -- The user whose permissions are requested.

        Returns {all_permission:
            course{id}: permisions
            assignment{id}: permissions
            general: permissions
        }"""
        perms = {}
        courses = user.participations.all()

        perms['general'] = permissions.serialize_general_permissions(user)

        for course in courses:
            perms['course' + str(course.id)] = permissions.serialize_course_permissions(user, course)

        assignments = set()
        for course in courses:
            for assignment in course.assignment_set.all():
                if user.has_permission('can_grade', assignment) or user.has_permission('can_have_journal', assignment):
                    assignments.add(assignment)

        for assignment in assignments:
            perms['assignment' + str(assignment.id)] = permissions.serialize_assignment_permissions(user, assignment)

        return perms


class PreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Preferences
        fields = ('user', 'grade_notifications', 'comment_notifications', 'upcoming_deadline_notifications',
                  'show_format_tutorial', 'hide_version_alert', 'grade_button_setting', 'comment_button_setting',
                  'auto_select_ungraded_entry', 'auto_proceed_next_journal')
        read_only_fields = ('user', )


class CourseSerializer(serializers.ModelSerializer):
    lti_linked = serializers.SerializerMethodField()

    class Meta:
        model = Course
        exclude = ('author', 'users', )
        read_only_fields = ('id', )

    def get_lti_linked(self, course):
        return course.has_lti_link()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ('id', 'course', 'lti_id')


class ParticipationSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    role = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = Participation
        fields = '__all__'
        read_only_fields = ('id', )

    def get_user(self, participation):
        return UserSerializer(participation.user, context=self.context).data

    def get_course(self, participation):
        return CourseSerializer(participation.course, context=self.context).data

    def get_role(self, participation):
        return RoleSerializer(participation.role, context=self.context).data

    def get_groups(self, participation):
        return GroupSerializer(participation.groups, many=True, context=self.context).data


class AssignmentDetailsSerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField()
    lti_count = serializers.SerializerMethodField()
    active_lti_course = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = ('id', 'name', 'description', 'points_possible', 'unlock_date', 'due_date', 'lock_date',
                  'is_published', 'course_count', 'lti_count', 'active_lti_course')
        read_only_fields = ('id', )

    def get_course_count(self, assignment):
        return assignment.courses.count()

    def get_lti_count(self, assignment):
        if 'user' in self.context and self.context['user'] and \
           self.context['user'].has_permission('can_edit_assignment', assignment):
            return len(assignment.lti_id_set)
        return None

    def get_active_lti_course(self, assignment):
        if 'user' in self.context and self.context['user'] and \
           self.context['user'].is_participant(assignment):
            c = assignment.get_active_course()
            if c:
                return {'cID': c.pk, 'name': c.name}
            return None
        return None


class AssignmentSerializer(serializers.ModelSerializer):
    deadline = serializers.SerializerMethodField()
    journal = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    course = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()
    course_count = serializers.SerializerMethodField()
    journals = serializers.SerializerMethodField()
    active_lti_course = serializers.SerializerMethodField()
    lti_courses = serializers.SerializerMethodField()

    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('id', )

    def get_deadline(self, assignment):
        # Student deadlines
        if 'user' in self.context and self.context['user'] and \
           self.context['user'].has_permission('can_have_journal', assignment):
            journal = Journal.objects.get(assignment=assignment, user=self.context['user'])
            deadline, name = self._get_student_deadline(journal, assignment)

            return {
                'date': deadline,
                'name': name
            }
        # Teacher deadline
        else:
            return {
                'date': self._get_teacher_deadline(assignment),
            }

    def _get_teacher_deadline(self, assignment):
        return assignment.journal_set \
            .filter(
                Q(node__entry__grade__grade__isnull=True) | Q(node__entry__grade__published=False),
                node__entry__isnull=False) \
            .values('node__entry__last_edited') \
            .aggregate(Min('node__entry__last_edited'))['node__entry__last_edited__min']

    def _get_student_deadline(self, journal, assignment):
        """Get student deadline.

        This function gets the first upcoming deadline.
        It checks for the first entrydeadline that still need to submitted and still can be, or for the first
        progressnode that is not yet fullfilled.
        """
        nodes = utils.get_sorted_nodes(journal)
        t_grade = 0
        deadline = None
        name = None

        for node in nodes:
            if node.entry:
                grade = node.entry.grade
            else:
                grade = None

            # Sum published grades to check if PROGRESS node is fullfiled
            if node.type in [Node.ENTRY, Node.ENTRYDEADLINE] and grade and grade.grade:
                if grade.published:
                    t_grade += grade.grade
            # Set the deadline to the first unfilled ENTRYDEADLINE node date
            elif node.type == Node.ENTRYDEADLINE and not node.entry and node.preset.due_date > timezone.now():
                deadline = node.preset.due_date
                name = node.preset.forced_template.name
                break
            # Set the deadline to first not completed PROGRESS node date
            elif node.type == Node.PROGRESS:
                if node.preset.target > t_grade and node.preset.due_date > timezone.now():
                    deadline = node.preset.due_date
                    name = "{:g}/{:g} points".format(t_grade, node.preset.target)
                    break

        # If no deadline is found, but the points possible has not been reached, make assignment due date the deadline
        if deadline is None and t_grade < assignment.points_possible:
            if journal.assignment.due_date or \
               journal.assignment.lock_date and journal.assignment.lock_date < timezone.now():
                deadline = assignment.due_date
                name = 'End of assignment'

        return deadline, name

    def get_journal(self, assignment):
        if not ('user' in self.context and self.context['user']):
            return None
        if not self.context['user'].has_permission('can_have_journal', assignment):
            return None
        return Journal.objects.get(assignment=assignment, user=self.context['user']).pk

    def get_journals(self, assignment):
        """Retrieves the journals of an assignment of the users who have the permission
        to own a journal.
        """
        if 'journals' in self.context and 'course' in self.context \
           and self.context['journals'] and self.context['course']:
            course = self.context['course']
            users = course.participation_set.filter(role__can_have_journal=True).values('user')
            journals = Journal.objects.filter(assignment=assignment, user__in=users)
            return JournalSerializer(journals, many=True, context=self.context).data
        else:
            return None

    def get_stats(self, assignment):
        if 'user' not in self.context or not self.context['user']:
            return None

        course = self._get_course(assignment)
        # Get the stats from only the course that its linked to, when no courses are supplied.
        users = User.objects.filter(
            participation__course=course, participation__role__can_have_journal=True
        )
        participation = Participation.objects.filter(user=self.context['user'], course=course)
        if participation.exists():
            participation = participation.first()
            if participation.groups and users.filter(participation__groups=participation.groups.first()).exists():
                users = users.filter(participation__groups=participation.groups.first())

        stats = {}
        journal_set = assignment.journal_set.filter(user__in=users)

        # Grader stats
        if self.context['user'].has_permission('can_grade', assignment):
            stats['needs_marking'] = journal_set \
                .filter(Q(node__entry__grade__grade=None) | Q(node__entry__grade=None),
                        node__entry__isnull=False).count()
            stats['unpublished'] = journal_set \
                .filter(node__entry__isnull=False, node__entry__grade__published=False,
                        node__entry__grade__grade__isnull=False).count()
        # Other stats
        stats['average_points'] = sum([journal.get_grade() for journal in journal_set]) / (journal_set.count() or 1)

        return stats

    def get_course(self, assignment):
        return CourseSerializer(self._get_course(assignment)).data

    def _get_course(self, assignment):
        if 'course' not in self.context or not self.context['course']:
            if assignment.active_lti_id:
                course = assignment.get_active_course()
            else:
                course = assignment.courses.order_by('-enddate').first()

        else:
            if not self.context['course'] in assignment.courses.all():
                raise VLEProgrammingError('Wrong course is supplied')
            elif not self.context['user'].is_participant(self.context['course']):
                raise VLEParticipationError(self.context['course'], self.context['user'])

            else:
                course = self.context['course']

        return course

    def get_courses(self, assignment):
        if 'course' in self.context and self.context['course']:
            return None
        return CourseSerializer(assignment.courses, many=True).data

    def get_active_lti_course(self, assignment):
        if 'user' in self.context and self.context['user'] and \
           self.context['user'].is_participant(assignment):
            c = assignment.get_active_course()
            if c:
                return {'cID': c.pk, 'name': c.name}
            return None
        return None

    def get_lti_courses(self, assignment):
        if 'user' in self.context and self.context['user'] and \
           self.context['user'].has_permission('can_edit_assignment', assignment):
            courses = assignment.courses.filter(assignment_lti_id_set__overlap=assignment.lti_id_set)
            return {c.pk: c.name for c in courses}
        return None

    def get_course_count(self, assignment):
        return assignment.courses.count()


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'
        read_only_fields = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    last_edited_by = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'entry', 'author', 'text', 'published', 'creation_date', 'last_edited', 'last_edited_by')
        read_only_fields = ('id', 'entry', 'author', 'timestamp')

    def get_author(self, comment):
        return UserSerializer(comment.author).data

    def get_last_edited_by(self, comment):
        return None if not comment.last_edited_by else comment.last_edited_by.full_name


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', 'course')


class JournalSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    needs_lti_link = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = ('id', 'bonus_points', 'grade', 'student', 'needs_lti_link', 'stats')
        read_only_fields = ('id', 'assignment', 'user', 'grade_url', 'sourcedid', 'grade')

    def get_grade(self, journal):
        return journal.get_grade()

    def get_needs_lti_link(self, journal):
        return journal.needs_lti_link()

    def get_student(self, journal):
        return UserSerializer(journal.user, context=self.context).data

    def get_stats(self, journal):
        return {
            'acquired_points': journal.get_grade(),
            'graded': journal.node_set.filter(entry__grade__grade__isnull=False).count(),
            'published': journal.node_set.filter(entry__grade__published=True).count(),
            'submitted': journal.node_set.filter(entry__isnull=False).count(),
        }


class FormatSerializer(serializers.ModelSerializer):
    presets = serializers.SerializerMethodField()
    templates = serializers.SerializerMethodField()

    class Meta:
        model = Format
        fields = ('id', 'templates', 'presets', )
        read_only_fields = ('id', )

    def get_templates(self, format):
        return TemplateSerializer(format.template_set.filter(archived=False).order_by('name'), many=True).data

    def get_presets(self, format):
        return PresetNodeSerializer(format.presetnode_set.all().order_by('due_date'), many=True).data


class PresetNodeSerializer(serializers.ModelSerializer):
    unlock_date = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()
    lock_date = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    template = serializers.SerializerMethodField()

    class Meta:
        model = PresetNode
        fields = ('id', 'description', 'type', 'unlock_date', 'due_date', 'lock_date', 'target', 'template')
        read_only_fields = ('id', 'type')

    def get_unlock_date(self, node):
        if node.type == Node.ENTRYDEADLINE and node.unlock_date is not None:
            return node.unlock_date.strftime('%Y-%m-%dT%H:%M')
        return None

    def get_due_date(self, node):
        return node.due_date.strftime('%Y-%m-%dT%H:%M:%S')

    def get_lock_date(self, node):
        if node.type == Node.ENTRYDEADLINE and node.lock_date is not None:
            return node.lock_date.strftime('%Y-%m-%dT%H:%M:%S')
        return None

    def get_target(self, node):
        if node.type == Node.PROGRESS:
            return node.target
        return None

    def get_template(self, node):
        if node.type == Node.ENTRYDEADLINE:
            return TemplateSerializer(node.forced_template).data
        return None


class EntrySerializer(serializers.ModelSerializer):
    template = serializers.SerializerMethodField()
    content = serializers.SerializerMethodField()
    editable = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Entry
        fields = ('id', 'creation_date', 'template', 'content', 'editable',
                  'grade', 'last_edited', 'comments')
        read_only_fields = ('id', 'template', 'creation_date', 'content', 'grade')

    def get_template(self, entry):
        return TemplateSerializer(entry.template).data

    def get_content(self, entry):
        return ContentSerializer(entry.content_set.all(), many=True).data

    def get_editable(self, entry):
        return entry.is_editable()

    def get_grade(self, entry):
        # TODO: Add permission can_view_grade
        if 'user' not in self.context or not self.context['user']:
            return None
        grade = entry.grade
        if grade and (grade.published or
                      self.context['user'].has_permission('can_grade', entry.node.journal.assignment)):
            return GradeSerializer(grade).data
        return None

    def get_comments(self, entry):
        if 'comments' not in self.context or not self.context['comments']:
            return None
        return CommentSerializer(Comment.objects.filter(entry=entry), many=True).data


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'entry', 'grade', 'published')
        read_only_fields = ('id', 'entry', 'grade', 'published')


class GradeHistorySerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()

    class Meta:
        model = Grade
        fields = ('grade', 'published', 'creation_date', 'author')
        read_only_fields = ('grade', 'published', 'creation_date', 'author')

    def get_author(self, grade):
        if grade.author is not None:
            return grade.author.full_name

        return 'Unknown or deleted account'


class TemplateSerializer(serializers.ModelSerializer):
    field_set = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ('id', )

    def get_field_set(self, template):
        return FieldSerializer(template.field_set.all(), many=True).data


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
        read_only_fields = ('id', )


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'
