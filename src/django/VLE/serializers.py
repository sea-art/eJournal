"""
Serializers.

Functions to convert certain data to other formats.
"""
from rest_framework import serializers
# import VLE.utils as utils
# import VLE.permissions as permissions
from VLE.models import User, Course, Node, Comment, Assignment, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'last_login', 'username', 'first_name', 'last_name', 'is_active',
                  'email', 'lti_id', 'profile_picture', 'is_teacher')
        read_only_fields = ('id', )


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('author', 'users', )
        read_only_fields = ('id', )
        depth = 1


class StudentAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('id', )


class TeacherAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        read_only_fields = ('id', )


class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = '__all__'
        read_only_fields = ('id', )


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', )

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
        read_only_fields = ('id', )

# def user_to_dict(user):
#     """Convert user object to dictionary."""
#     return {
#         'name': user.username,
#         'email': user.email,
#         'lti_id': user.lti_id,
#         'is_superuser': user.is_superuser,
#         'grade_notifications': user.grade_notifications,
#         'comment_notifications': user.comment_notifications,
#         'picture': user.profile_picture,
#         'uID': user.id,
#         'first_name': user.first_name,
#         'last_name': user.last_name
#     } if user else None
#
#
# def participation_to_dict(participation):
#     """Convert participation to a dictionary.
#
#     Parameters
#     ----------
#     participation : Participation
#         The participation to convert.
#
#     Returns
#     -------
#     dictionary
#         Dictionary of the role and user dictionaries.
#
#     """
#     role_dict = {'role': participation.role.name}
#     user_dict = user_to_dict(participation.user)
#
#     return {**role_dict, **user_dict} if participation else None
#
#
# def course_to_dict(course):
#     """Convert course to a dictionary."""
#     return {
#         'cID': course.id,
#         'name': course.name,
#         'auth': user_to_dict(course.author),
#         'startdate': course.startdate,
#         'enddate': course.enddate,
#         'abbr': course.abbreviation
#     } if course else None
#
#
# def student_assignment_to_dict(assignment, user):
#     """Convert a student assignment to a dictionary."""
#     if not assignment:
#         return None
#     try:
#         journal = Journal.objects.get(assignment=assignment, user=user)
#     except Journal.DoesNotExist:
#         journal = None
#
#     assignment_dict = assignment_to_dict(assignment)
#     assignment_dict['journal'] = journal_to_dict(journal) if journal else None
#
#     return assignment_dict
#
#
# def assignment_to_dict(assignment):
#     """Convert assignment to dictionary."""
#     return {
#         'aID': assignment.id,
#         'name': assignment.name,
#         'description': assignment.description,
#         'auth': user_to_dict(assignment.author),
#     } if assignment else None
#
#
# def journal_to_dict(journal):
#     """Convert a journal to a dictionary."""
#     entries = utils.get_journal_entries(journal)
#     return {
#         'jID': journal.id,
#         'student': user_to_dict(journal.user),
#         'stats': {
#             'acquired_points': utils.get_acquired_grade(entries, journal),
#             'graded': utils.get_graded_count(entries),
#             'submitted': utils.get_submitted_count(entries),
#             'total_points': utils.get_max_points(journal),
#         }
#     } if journal else None
#
#
# def add_node_dict(journal):
#     """Convert a add_node to a dictionary."""
#     if journal.assignment.format.available_templates.count() == 0:
#         return None
#
#     return {
#         'type': 'a',
#         'nID': -1,
#         'templates': [template_to_dict(template) for template in journal.assignment.format.available_templates.all()]
#     } if journal else None
#
#
# def node_to_dict(node, user):
#     """Convert a node to a dictionary."""
#     if node.type == Node.ENTRY:
#         return entry_node_to_dict(node, user)
#     elif node.type == Node.ENTRYDEADLINE:
#         return entry_deadline_to_dict(node, user)
#     elif node.type == Node.PROGRESS:
#         return progress_to_dict(node)
#     return None
#
#
# def entry_node_to_dict(node, user):
#     """Convert an entrynode to a dictionary."""
#     return {
#         'type': node.type,
#         'nID': node.id,
#         'jID': node.id,
#         'entry': entry_to_dict(node.entry, user),
#     } if node else None
#
#
# def entry_deadline_to_dict(node, user):
#     """Convert entrydeadline to a dictionary."""
#     return {
#         'type': node.type,
#         'nID': node.id,
#         'jID': node.id,
#         'deadline': node.preset.deadline.strftime('%Y-%m-%d %H:%M'),
#         'template': template_to_dict(node.preset.forced_template),
#         'entry': entry_to_dict(node.entry, user),
#     } if node else None
#
#
# def progress_to_dict(node):
#     """Convert progress node to dictionary."""
#     return {
#         'type': node.type,
#         'nID': node.id,
#         'jID': node.id,
#         'deadline': node.preset.deadline.strftime('%Y-%m-%d %H:%M'),
#         'target': node.preset.target,
#     } if node else None
#
#
# def entry_to_dict(entry, user):
#     """Convert entry to dictionary."""
#     if not entry:
#         return None
#
#     data = {
#         'eID': entry.id,
#         'createdate': entry.createdate.strftime('%Y-%m-%d %H:%M'),
#         'published': entry.published,
#         'template': template_to_dict(entry.template),
#         'content': [content_to_dict(content) for content in entry.content_set.all()],
#         'editable': True
#     }
#
#     if entry.grade is not None:
#         data['editable'] = False
#
#     assignment = entry.node.journal.assignment
#     if permissions.has_assignment_permission(user, assignment, 'can_grade_journal') or entry.published:
#         data['grade'] = entry.grade
#
#     return data
#
#
# def export_entry_to_dict(entry):
#     """Convert entry to exportable dictionary."""
#     if not entry:
#         return None
#
#     data = {
#         'createdate': entry.createdate.strftime('%d-%m-%Y %H:%M'),
#         'grade': entry.grade
#     }
#
#     # Add the field-content combinations.
#     for field, content in zip(entry.template.field_set.all(), entry.content_set.all()):
#         data.update({field.title: content.data})
#
#     # Add the comments.
#     comments = [{entrycomment.author.username: entrycomment.text}
#                 for entrycomment in Comment.objects.filter(entry=entry)]
#     data.update({'comments': comments})
#
#     return data
#
#
# def template_to_dict(template):
#     """Convert template to dictionary."""
#     return {
#         'tID': template.id,
#         'name': template.name,
#         'fields': [field_to_dict(field) for field in template.field_set.all()],
#     } if template else None
#
#
# def field_to_dict(field):
#     """Convert field to dictionary."""
#     return {
#         'tag': field.id,
#         'type': field.type,
#         'title': field.title,
#         'location': field.location,
#     } if field else None
#
#
# def content_to_dict(content):
#     """Convert content to dictionary."""
#     return {
#         'tag': content.field.pk,
#         'data': content.data,
#     } if content else None
#
#
# def format_to_dict(format):
#     """Convert format to dictionary."""
#     return {
#         'max_points': format.max_points,
#         'unused_templates': [template_to_dict(template) for template in format.unused_templates.all()],
#         'templates': [template_to_dict(template) for template in format.available_templates.all()],
#         'presets': [preset_to_dict(preset) for preset in format.presetnode_set.all().order_by('deadline')],
#     } if format else None
#
#
# def preset_to_dict(preset):
#     """Convert preset node to dictionary."""
#     if not preset:
#         return None
#
#     base = {
#         'pID': preset.id,
#         'type': preset.type,
#         'deadline': preset.deadline.strftime('%Y-%m-%d %H:%M'),
#     }
#
#     if preset.type == Node.PROGRESS:
#         result = {**base, **{'target': preset.target}}
#     elif preset.type == Node.ENTRYDEADLINE:
#         result = {**base, **{'template': template_to_dict(preset.forced_template)}}
#
#     return result
#
#
# def entrycomment_to_dict(entrycomment):
#     """Convert entrycomment to dictionary."""
#     return {
#         'eID': entrycomment.entry.id,
#         'author': user_to_dict(entrycomment.author),
#         'text': entrycomment.text,
#     } if entrycomment else None
#
#
# def role_to_dict(role):
#     """Convert role to dictionary."""
#     return {
#         'name': role.name,
#         'cID': role.course.pk,
#         'permissions': {
#             'can_edit_course_roles': int(role.can_edit_course_roles),
#             'can_view_course_participants': int(role.can_view_course_participants),
#             'can_edit_course': int(role.can_edit_course),
#             'can_delete_course': int(role.can_delete_course),
#             'can_add_assignment': int(role.can_add_assignment),
#             'can_view_assignment_participants': int(role.can_view_assignment_participants),
#             'can_delete_assignment': int(role.can_delete_assignment),
#             'can_publish_assigment_grades': int(role.can_publish_assigment_grades),
#             'can_grade_journal': int(role.can_grade_journal),
#             'can_publish_journal_grades': int(role.can_publish_journal_grades),
#             'can_edit_journal': int(role.can_edit_journal),
#             'can_comment_journal': int(role.can_comment_journal)
#         }
#     } if role else None
