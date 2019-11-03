"""
models.py.

Database file
"""
import os

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import now

import VLE.permissions as permissions
from VLE.utils import sanitization
from VLE.utils.error_handling import (VLEParticipationError, VLEPermissionError, VLEProgrammingError,
                                      VLEUnverifiedEmailError)
from VLE.utils.file_handling import get_feedback_file_path, get_path


class Instance(models.Model):
    """Global settings for the running instance."""
    allow_standalone_registration = models.BooleanField(
        default=True
    )
    name = models.TextField(
        default='eJournal'
    )

    def to_string(self, user=None):
        return self.name


class UserFile(models.Model):
    """UserFile.

    UserFile is a file uploaded by the user stored in MEDIA_ROOT/uID/aID/<file>
    - author: The user who uploaded the file.
    - file_name: The name of the file (no parts of the path to the file included).
    - creation_date: The time and date the file was uploaded.
    - content_type: The content type supplied by the user (unvalidated).
    - assignment: The assignment that the UserFile is linked to.
    - node: The node that the UserFile is linked to.
    - entry: The entry that the UserFile is linked to.
    - content: The content that UserFile is linked to.

    Note that deleting the assignment, node or content will also delete the UserFile.
    UserFiles uploaded initially have no node or content set, and are considered temporary until the journal post
    is made and the corresponding node and content are set.
    """
    file = models.FileField(
        null=False,
        upload_to=get_path
    )
    file_name = models.TextField(
        null=False
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        null=False
    )
    content_type = models.TextField(
        null=False
    )
    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE,
        null=False
    )
    node = models.ForeignKey(
        'Node',
        on_delete=models.CASCADE,
        null=True
    )
    entry = models.ForeignKey(
        'Entry',
        on_delete=models.CASCADE,
        null=True
    )
    content = models.ForeignKey(
        'Content',
        on_delete=models.CASCADE,
        null=True
    )
    creation_date = models.DateTimeField(editable=False)
    last_edited = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_date = timezone.now()
        self.last_edited = timezone.now()

        return super(UserFile, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.file.delete()
        super(UserFile, self).delete(*args, **kwargs)

    def to_string(self, user=None):
        return "UserFile"


@receiver(models.signals.post_delete, sender=UserFile)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Deletes file from filesystem when corresponding `UserFile` object is deleted."""
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


class User(AbstractUser):
    """User.

    User is an entity in the database with the following features:
    - full_name: full name of the user
    - email: email of the user.
    - verified_email: Boolean to indicate if the user has validated their email address.
    - USERNAME_FIELD: username of the username.
    - password: the hash of the password of the user.
    - lti_id: the DLO id of the user.
    """

    full_name = models.CharField(
        null=False,
        max_length=200
    )
    email = models.EmailField(
        blank=True,
        unique=True,
        null=True,
    )
    verified_email = models.BooleanField(
        default=False
    )
    lti_id = models.TextField(
        null=True,
        unique=True,
        blank=True,
    )
    profile_picture = models.TextField(
        null=True
    )
    is_teacher = models.BooleanField(
        default=False
    )
    feedback_file = models.FileField(
        null=True,
        blank=True,
        upload_to=get_feedback_file_path
    )
    is_test_student = models.BooleanField(
        default=False
    )

    def check_permission(self, permission, obj=None, message=None):
        """
        Throws a VLEPermissionError when the user does not have the specified permission, as defined by
        has_permission.
        """
        if not self.has_permission(permission, obj):
            raise VLEPermissionError(permission, message)

    def has_permission(self, permission, obj=None):
        """
        Returns whether the user has the given permission.
        If obj is None, it tests the general permissions.
        If obj is a Course, it tests the course permissions.
        If obj is an Assignment, it tests the assignment permissions.
        Raises a VLEProgramming error when misused.
        """
        if obj is None:
            return permissions.has_general_permission(self, permission)
        if isinstance(obj, Course):
            return permissions.has_course_permission(self, permission, obj)
        if isinstance(obj, Assignment):
            return permissions.has_assignment_permission(self, permission, obj)
        raise VLEProgrammingError("Permission object must be of type None, Course or Assignment.")

    def check_verified_email(self):
        if not self.verified_email:
            raise VLEUnverifiedEmailError()

    def check_participation(self, obj):
        if not self.is_participant(obj):
            raise VLEParticipationError(obj, self)

    def is_participant(self, obj):
        if self.is_superuser:
            return True
        if isinstance(obj, Course):
            return Course.objects.filter(pk=obj.pk, users=self).exists()
        if isinstance(obj, Assignment):
            return Assignment.objects.filter(pk=obj.pk, courses__users=self).exists()
        raise VLEProgrammingError("Participant object must be of type Course or Assignment.")

    def check_can_view(self, obj):
        if not self.can_view(obj):
            raise VLEPermissionError(message='You are not allowed to view {}'.format(obj.to_string()))

    def can_view(self, obj):
        if self.is_superuser:
            return True

        if isinstance(obj, Course):
            return self.is_participant(obj)

        elif isinstance(obj, Assignment):
            if self.is_participant(obj):
                return obj.is_published or self.has_permission('can_view_unpublished_assignment', obj)
            return False
        elif isinstance(obj, Journal):

            if obj.user != self:
                return self.has_permission('can_view_all_journals', obj.assignment)
            else:
                return self.has_permission('can_have_journal', obj.assignment)

        elif isinstance(obj, Comment):
            if not self.can_view(obj.entry.node.journal):
                return False
            if obj.published:
                return True
            return self.has_permission('can_grade', obj.entry.node.journal.assignment)

        return False

    def check_can_edit(self, obj):
        if not permissions.can_edit(self, obj):
            raise VLEPermissionError(message='You are not allowed to edit {}'.format(str(obj)))

    def to_string(self, user=None):
        if user is None:
            return "User"
        if not (self.is_superuser or self == user or permissions.is_user_supervisor_of(user, self)):
            return "User"
        return self.username + " (" + str(self.pk) + ")"

    def save(self, *args, **kwargs):
        if not self.email and not self.is_test_student:
            raise ValidationError('A legitimate user requires an email adress.')

        if self._state.adding:
            if self.is_test_student and settings.LTI_TEST_STUDENT_FULL_NAME not in self.full_name:
                raise ValidationError('Test user\'s full name deviates on creation.')
        else:
            pre_save = User.objects.get(pk=self.pk)
            if pre_save.is_test_student and not self.is_test_student:
                raise ValidationError('A test user is expected to remain a test user.')

        # Enforce unique constraint
        if self.email == '':
            self.email = None

        super(User, self).save(*args, **kwargs)


@receiver(models.signals.post_save, sender=User)
def create_user_preferences(sender, instance, created, **kwargs):
    """Create matching preferences whenever a user object is created."""
    if created:
        Preferences.objects.create(user=instance)


@receiver(models.signals.post_delete, sender=User)
def auto_delete_feedback_file_on_user_delete(sender, instance, **kwargs):
    """Deletes feedback file from filesystem when corresponding `User` object is deleted."""
    if instance.feedback_file:
        if os.path.isfile(instance.feedback_file.path):
            os.remove(instance.feedback_file.path)


class Preferences(models.Model):
    """Preferences.

    Describes the preferences of a user:
    - show_format_tutorial: whether or not to show the assignment format tutorial.
    - grade_notifications: whether or not to receive grade notifications via email.
    - comment_notifications: whether or not to receive comment notifications via email.
    - upcoming_deadline_notifications: whether or not to receive upcoming deadline notifications via email.
    - hide_version_alert: latest version number for which a version alert has been dismissed.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    grade_notifications = models.BooleanField(
        default=True
    )
    comment_notifications = models.BooleanField(
        default=True
    )
    upcoming_deadline_notifications = models.BooleanField(
        default=True
    )
    show_format_tutorial = models.BooleanField(
        default=True
    )
    auto_select_ungraded_entry = models.BooleanField(
        default=True
    )
    auto_proceed_next_journal = models.BooleanField(
        default=False
    )
    hide_version_alert = models.TextField(
        max_length=10,
        null=True,
    )
    SAVE = 's'
    PUBLISH = 'p'
    GRADE_BUTTON_OPTIONS = (
        (SAVE, 's'),
        (PUBLISH, 'p'),
    )
    grade_button_setting = models.TextField(
        max_length=1,
        choices=GRADE_BUTTON_OPTIONS,
        default=PUBLISH,
    )
    PUBLISH_AND_PUBLISH_GRADE = 'g'
    COMMENT_SEND_BUTTON_OPTIONS = (
        (SAVE, 's'),
        (PUBLISH, 'p'),
        (PUBLISH_AND_PUBLISH_GRADE, 'g'),
    )
    comment_button_setting = models.TextField(
        max_length=2,
        choices=COMMENT_SEND_BUTTON_OPTIONS,
        default=SAVE,
    )

    def to_string(self, user=None):
        return "Preferences"


class Course(models.Model):
    """Course.

    A Course entity has the following features:
    - name: name of the course.
    - author: the creator of the course.
    - abbreviation: a max three letter abbreviation of the course name.
    - startdate: the date that the course starts.
    - active_lti_id: (optional) the active VLE id of the course linked through LTI which receives grade updates.
    - lti_id_set: (optional) the set of VLE lti_id_set which permit basic access.
    """

    name = models.TextField()
    abbreviation = models.TextField(
        max_length=10,
        default='XXXX',
    )

    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True
    )

    users = models.ManyToManyField(
        'User',
        related_name='participations',
        through='Participation',
        through_fields=('course', 'user'),
    )

    startdate = models.DateField(
        null=True,
    )
    enddate = models.DateField(
        null=True,
    )

    active_lti_id = models.TextField(
        null=True,
        unique=True,
        blank=True,
    )

    # These LTI assignments belong to this course.
    assignment_lti_id_set = ArrayField(
        models.TextField(),
        default=list,
    )

    def set_assignment_lti_id_set(self, lti_id):
        if lti_id not in self.assignment_lti_id_set:
            self.assignment_lti_id_set.append(lti_id)

    def has_lti_link(self):
        return self.active_lti_id is not None

    def to_string(self, user=None):
        if user is None:
            return "Course"
        if not user.can_view(self):
            return "Course"

        return self.name + " (" + str(self.pk) + ")"


class Group(models.Model):
    """Group.

    A Group entity has the following features:
    - name: the name of the group
    - course: the course where the group belongs to
    """
    name = models.TextField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    lti_id = models.TextField(
        null=True,
    )

    class Meta:
        """Meta data for the model: unique_together."""
        unique_together = ('lti_id', 'course')

    def to_string(self, user=None):
        if user is None:
            return "Group"
        if not user.can_view(self.course):
            return "Group"
        return "{} ({})".format(self.name, self.pk)


class Role(models.Model):
    """Role.

    A complete overview of the role requirements can be found here:
    https://docs.google.com/spreadsheets/d/1M7KnEKL3cG9PMWfQi9HIpRJ5xUMou4Y2plnRgke--Tk

    A role defines the permissions of a user group within a course.
    - name: name of the role
    - list of permissions (can_...)
    """
    name = models.TextField()

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE
    )

    can_edit_course_details = models.BooleanField(default=False)
    can_delete_course = models.BooleanField(default=False)
    can_edit_course_roles = models.BooleanField(default=False)
    can_view_course_users = models.BooleanField(default=False)
    can_add_course_users = models.BooleanField(default=False)
    can_delete_course_users = models.BooleanField(default=False)
    can_add_course_user_group = models.BooleanField(default=False)
    can_delete_course_user_group = models.BooleanField(default=False)
    can_edit_course_user_group = models.BooleanField(default=False)
    can_add_assignment = models.BooleanField(default=False)
    can_delete_assignment = models.BooleanField(default=False)

    can_edit_assignment = models.BooleanField(default=False)
    can_view_all_journals = models.BooleanField(default=False)
    can_grade = models.BooleanField(default=False)
    can_publish_grades = models.BooleanField(default=False)
    can_view_grade_history = models.BooleanField(default=False)
    can_have_journal = models.BooleanField(default=False)
    can_comment = models.BooleanField(default=False)
    can_edit_staff_comment = models.BooleanField(default=False)
    can_view_unpublished_assignment = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.can_add_course_users and not self.can_view_course_users:
            raise ValidationError('A user needs to be able to view course users in order to add them.')

        if self.can_delete_course_users and not self.can_view_course_users:
            raise ValidationError('A user needs to be able to view course users in order to remove them.')

        if self.can_edit_course_user_group and not self.can_view_course_users:
            raise ValidationError('A user needs to be able to view course users in order to manage user groups.')

        if self.can_view_all_journals and self.can_have_journal:
            raise ValidationError('Teaching staff is not allowed to have a journal in their own course.')

        if self.can_grade and not self.can_view_all_journals:
            raise ValidationError('A user needs to be able to view journals in order to grade them.')

        if self.can_publish_grades and not (self.can_view_all_journals and self.can_grade):
            raise ValidationError('A user needs to be able to view and grade journals in order to publish grades.')

        if self.can_view_grade_history and not (self.can_view_all_journals and self.can_grade):
            raise ValidationError('A user needs to be able to view and grade journals in order to see a history\
                                   of grades.')

        if self.can_comment and not (self.can_view_all_journals or self.can_have_journal):
            raise ValidationError('A user requires a journal to comment on.')

        if self.can_edit_staff_comment and self.can_have_journal:
            raise ValidationError('Users who can edit staff comments are not allowed to have a journal themselves.')

        if self.can_edit_staff_comment and not self.can_comment:
            raise ValidationError('A user needs to be able to comment in order to edit other comments.')

        super(Role, self).save(*args, **kwargs)

    def to_string(self, user=None):
        if user is None:
            return "Role"
        if not user.can_view(self.course):
            return "Role"

        return "{} ({})".format(self.name, self.pk)

    class Meta:
        """Meta data for the model: unique_together."""

        unique_together = ('name', 'course',)


class Participation(models.Model):
    """Participation.

    A participation defines the way a user interacts within a certain course.
    The user is now linked to the course, and has a set of permissions
    associated with its role.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        related_name='role',
    )
    groups = models.ManyToManyField(
        Group,
        default=None,
    )

    class Meta:
        """Meta data for the model: unique_together."""

        unique_together = ('user', 'course',)

    def to_string(self, user=None):
        if user is None:
            return "Participation"
        if not user.can_view(self.course):
            return "Participation"

        return "user: {}, course: {}, role: {}".format(
            self.user.to_string(user), self.course.to_string(user), self.role.to_string(user))


class Assignment(models.Model):
    """Assignment.

    An Assignment entity has the following features:
    - name: name of the assignment.
    - description: description for the assignment.
    - courses: a foreign key linked to the courses this assignment
    is part of.
    - format: a one-to-one key linked to the format this assignment
    holds. The format determines how a students' journal is structured.
    - active_lti_id: (optional) the active VLE id of the assignment linked through LTI which receives grade updates.
    - lti_id_set: (optional) the set of VLE assignment lti_id_set which permit basic access.
    """

    name = models.TextField()
    description = models.TextField(
        null=True,
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True
    )
    is_published = models.BooleanField(default=False)
    points_possible = models.IntegerField(
        'points_possible',
        default=10
    )
    unlock_date = models.DateTimeField(
        'unlock_date',
        null=True,
        blank=True
    )
    due_date = models.DateTimeField(
        'due_date',
        null=True,
        blank=True
    )
    lock_date = models.DateTimeField(
        'lock_date',
        null=True,
        blank=True
    )
    courses = models.ManyToManyField(Course)

    format = models.OneToOneField(
        'Format',
        on_delete=models.CASCADE
    )

    active_lti_id = models.TextField(
        null=True,
        unique=True,
        blank=True,
    )
    lti_id_set = ArrayField(
        models.TextField(),
        default=list,
    )

    def has_lti_link(self):
        return self.active_lti_id is not None

    def is_locked(self):
        return self.unlock_date and self.unlock_date > now() or self.lock_date and self.lock_date < now()

    def save(self, *args, **kwargs):
        self.description = sanitization.strip_script_tags(self.description)

        active_lti_id_modified = False

        # Instance is being created (not modified)
        if self._state.adding:
            active_lti_id_modified = self.active_lti_id is not None
        else:
            if self.pk:
                pre_save = Assignment.objects.get(pk=self.pk)
                active_lti_id_modified = pre_save.active_lti_id != self.active_lti_id
            # A copy is being made of the original instance
            else:
                self.active_lti_id = None
                self.lti_id_set = []

        if active_lti_id_modified:
            # Reset all sourcedid if the active lti id is updated.
            Journal.objects.filter(assignment=self.pk).update(sourcedid=None, grade_url=None)

            if self.active_lti_id is not None and self.active_lti_id not in self.lti_id_set:
                self.lti_id_set.append(self.active_lti_id)

            other_assignments_with_lti_id_set = Assignment.objects.filter(
                lti_id_set__contains=[self.active_lti_id]).exclude(pk=self.pk)
            if other_assignments_with_lti_id_set.exists():
                raise ValidationError(
                    "A lti_id should be unique, and only part of a single assignment's lti_id_set.")

        return super(Assignment, self).save(*args, **kwargs)

    def get_active_lti_course(self):
        """"Query for retrieving the course which matches the active lti id of the assignment."""
        courses = self.courses.filter(assignment_lti_id_set__contains=[self.active_lti_id])
        return courses.first()

    def get_active_course(self):
        """"Query for retrieving the course which is most relevant to the assignment."""
        # Get matching LTI course if possible
        course = self.get_active_lti_course()
        if course is not None:
            return course

        # Else get course that started the most recent
        course = self.courses.filter(startdate__lt=timezone.now()).order_by('-startdate').first()
        if course is not None:
            return course

        # Else get the course that starts the soonest
        return self.courses.order_by('startdate').first()

    def get_course_lti_id(self, course):
        """Gets the assignment lti_id that belongs to the course assignment pair if it exists."""
        if not isinstance(course, Course):
            raise VLEProgrammingError("Expected instance of type Course.")

        intersection = list(set(self.lti_id_set).intersection(course.assignment_lti_id_set))
        return intersection[0] if intersection else None

    def can_unpublish(self):
        return not (self.is_published and Entry.objects.filter(node__journal__assignment=self).exists())

    def to_string(self, user=None):
        if user is None:
            return "Assignment"
        if not user.can_view(self):
            return "Assignment"

        return "{} ({})".format(self.name, self.pk)


class Journal(models.Model):
    """Journal.

    A journal is a collection of Nodes that holds the student's
    entries, deadlines and more. It contains the following:
    - assignment: a foreign key linked to an assignment.
    - user: a foreign key linked to a user.
    """

    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
    )

    sourcedid = models.TextField(
        'sourcedid',
        null=True
    )
    grade_url = models.TextField(
        'grade_url',
        null=True
    )

    bonus_points = models.FloatField(
        default=0,
    )

    def get_grade(self):
        return self.bonus_points + (self.node_set.filter(entry__grade__published=True)
                                    .values('entry__grade__grade')
                                    .aggregate(Sum('entry__grade__grade'))['entry__grade__grade__sum'] or 0)

    # NOTE: Any suggestions for a clear warning msg for all cases?
    outdated_link_warning_msg = 'This journal has an outdated LMS uplink and can no longer be edited. Visit  ' \
        + 'eJournal from an updated LMS connection.'

    def needs_lti_link(self):
        return self.sourcedid is None and self.assignment.active_lti_id is not None

    def to_string(self, user=None):
        if user is None:
            return "Journal"
        if not user.can_view(self):
            return "Journal"

        return "the {0} journal of {1}".format(self.assignment.name, self.user.username)

    class Meta:
        """A class for meta data.

        - unique_together: assignment and user must be unique together.
        """

        unique_together = ('assignment', 'user',)


class Node(models.Model):
    """Node.

    The Node is an Timeline component.
    It can represent many things.
    There are three types of nodes:
    -Progress
        A node that merely is a deadline,
        and contains no entry. This deadline
        contains a 'target point amount'
        which should be reached before the
        due date has passed.
        This type of node has to be predefined in
        the Format. In the Format it is assigned a
        due date and a 'target point amount'.
    -Entry
        A node that is merely an entry,
        and contains no deadline. The entry
        can count toward a total
        'received point amount' which is deadlined
        by one or more Progress nodes.
        This type node can be created by the student
        an unlimited amount of times. It holds one
        of the by format predefined 'global templates'.
    -Entrydeadline
        A node that is both an entry and a deadline.
        This node is entirely separate from the
        Progress and Entry node.
        This type of node has to be predefined in
        the Format. In the Format it is assigned an
        unlock/lock date, a due date and a 'forced template'.
    """

    PROGRESS = 'p'
    ENTRY = 'e'
    ENTRYDEADLINE = 'd'
    ADDNODE = 'a'
    TYPES = (
        (PROGRESS, 'progress'),
        (ENTRY, 'entry'),
        (ENTRYDEADLINE, 'entrydeadline'),
    )

    type = models.TextField(
        max_length=4,
        choices=TYPES,
    )

    entry = models.OneToOneField(
        'Entry',
        null=True,
        on_delete=models.SET_NULL,
    )

    journal = models.ForeignKey(
        'Journal',
        on_delete=models.CASCADE,
    )

    preset = models.ForeignKey(
        'PresetNode',
        null=True,
        on_delete=models.SET_NULL,
    )

    def to_string(self, user=None):
        return "Node"


class Format(models.Model):
    """Format.

    Format of a journal.
    The format determines how a students' journal is structured.
    See PresetNodes for attached 'default' nodes.
    """

    def to_string(self, user=None):
        return "Format"


class PresetNode(models.Model):
    """PresetNode.

    A preset node is a node that has been pre-defined by the teacher.
    It contains the following features:
    - description: user defined text description of the preset node.
    - type: the type of the preset node (progress or entrydeadline node).
    - unlock_date: the date from which the preset node can be filled in.
    - due_date: the due date for this preset node.
    - lock_date: the date after which the preset node can no longer be fulfilled.
    - forced_template: the template for this preset node - null if PROGRESS node.
    - format: a foreign key linked to a format.
    """

    TYPES = (
        (Node.PROGRESS, 'progress'),
        (Node.ENTRYDEADLINE, 'entrydeadline'),
    )

    description = models.TextField(
        null=True,
    )

    type = models.TextField(
        max_length=4,
        choices=TYPES,
    )

    target = models.FloatField(
        null=True,
    )

    unlock_date = models.DateTimeField(
        null=True
    )

    due_date = models.DateTimeField()

    lock_date = models.DateTimeField(
        null=True
    )

    forced_template = models.ForeignKey(
        'Template',
        on_delete=models.SET_NULL,
        null=True,
    )

    format = models.ForeignKey(
        'Format',
        on_delete=models.CASCADE
    )

    def is_locked(self):
        return self.unlock_date is not None and self.unlock_date > now() or self.lock_date and self.lock_date < now()

    def to_string(self, user=None):
        return "PresetNode"


class Entry(models.Model):
    """Entry.

    An Entry has the following features:
    - creation_date: the date and time when the entry was posted.
    - last_edited: the date and time when the etry was last edited
    """
    NEED_SUBMISSION = 'Submission needs to be sent to VLE'
    SEND_SUBMISSION = 'Submission is successfully received by VLE'
    GRADING = 'Grade needs to be sent to VLE'
    LINK_COMPLETE = 'Everything is sent to VLE'
    TYPES = (
        (NEED_SUBMISSION, 'entry_submission'),
        (SEND_SUBMISSION, 'entry_submitted'),
        (GRADING, 'grade_submission'),
        (LINK_COMPLETE, 'done'),
    )

    # TODO Should not be nullable
    template = models.ForeignKey(
        'Template',
        on_delete=models.SET_NULL,
        null=True,
    )
    grade = models.ForeignKey(
        'Grade',
        on_delete=models.SET_NULL,
        related_name='+',
        null=True,
    )
    creation_date = models.DateTimeField(editable=False)
    last_edited = models.DateTimeField()

    vle_coupling = models.TextField(
        default=NEED_SUBMISSION,
        choices=TYPES,
    )

    def is_locked(self):
        return (self.node.preset and self.node.preset.is_locked()) or self.node.journal.assignment.is_locked()

    def is_editable(self):
        return not self.is_graded() and not self.is_locked()

    def is_graded(self):
        return not (self.grade is None or self.grade.grade is None)

    def save(self, *args, **kwargs):
        if not self.pk:
            now = timezone.now()
            self.creation_date = now
            self.last_edited = now

        return super(Entry, self).save(*args, **kwargs)

    def to_string(self, user=None):
        return "Entry"


class Grade(models.Model):
    """Grade.

    Used to keep a history of grades.
    """
    entry = models.ForeignKey(
        'Entry',
        editable=False,
        related_name='+',
        on_delete=models.CASCADE
    )
    grade = models.FloatField(
        null=True,
        editable=False
    )
    published = models.BooleanField(
        default=False,
        editable=False
    )
    creation_date = models.DateTimeField(
        editable=False,
        auto_now_add=True
    )
    author = models.ForeignKey(
        'User',
        null=True,
        editable=False,
        on_delete=models.SET_NULL
    )

    def save(self, *args, **kwargs):
        self.creation_date = timezone.now()
        return super(Grade, self).save(*args, **kwargs)

    def to_string(self, user=None):
        return "Grade"


class Counter(models.Model):
    """Counter.

    A single counter class which can be used to keep track of incremental values
    which do not belong to another object like the message ID for LTI messages.
    """

    name = models.TextField(
        null=False
    )
    count = models.IntegerField(
        default=0
    )

    def to_string(self, user=None):
        return self.name + " is on " + self.count


class Template(models.Model):
    """Template.

    A template for an Entry.
    """

    name = models.TextField()

    format = models.ForeignKey(
        'Format',
        on_delete=models.CASCADE
    )

    preset_only = models.BooleanField(
        default=False
    )

    archived = models.BooleanField(
        default=False
    )

    def to_string(self, user=None):
        return "Template"


class Field(models.Model):
    """Field.

    Defines the fields of an Template
    """

    TEXT = 't'
    RICH_TEXT = 'rt'
    IMG = 'i'
    FILE = 'f'
    VIDEO = 'v'
    PDF = 'p'
    URL = 'u'
    DATE = 'd'
    DATETIME = 'dt'
    SELECTION = 's'
    FILE_TYPES = [PDF, FILE, IMG]
    TYPES = (
        (TEXT, 'text'),
        (RICH_TEXT, 'rich text'),
        (IMG, 'img'),
        (PDF, 'pdf'),
        (FILE, 'file'),
        (VIDEO, 'vid'),
        (URL, 'url'),
        (DATE, 'date'),
        (DATETIME, 'datetime'),
        (SELECTION, 'selection')
    )
    type = models.TextField(
        max_length=4,
        choices=TYPES,
        default=TEXT,
    )
    title = models.TextField()
    description = models.TextField(
        null=True
    )
    options = models.TextField(
        null=True
    )
    location = models.IntegerField()
    template = models.ForeignKey(
        'Template',
        on_delete=models.CASCADE
    )
    required = models.BooleanField()

    def to_string(self, user=None):
        return "{} ({})".format(self.title, self.id)


class Content(models.Model):
    """Content.

    Defines the content of an Entry
    """

    entry = models.ForeignKey(
        'Entry',
        on_delete=models.CASCADE
    )
    # Question: Why can this be null?
    field = models.ForeignKey(
        'Field',
        on_delete=models.SET_NULL,
        null=True
    )
    data = models.TextField(
        null=True
    )

    def save(self, *args, **kwargs):
        self.data = sanitization.strip_script_tags(self.data)

        return super(Content, self).save(*args, **kwargs)

    def to_string(self, user=None):
        return "Content"


class Comment(models.Model):
    """Comment.

    Comments contain the comments given to the entries.
    It is linked to a single entry with a single author and the comment text.
    """

    entry = models.ForeignKey(
        'Entry',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True
    )
    text = models.TextField()
    published = models.BooleanField(
        default=True
    )
    creation_date = models.DateTimeField(editable=False)
    last_edited = models.DateTimeField()
    last_edited_by = models.ForeignKey(
        'User',
        related_name='last_edited_by',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )

    def can_edit(self, user):
        """
        Returns whether the given user is allowed to edit the comment:
            - Has to be the author or super_user
            - Otheriwse has to have the permission 'can_edit_staff_comment' and edit a non journal author comment.
              Because staff members can't have a journal themselves, checking if the author is not the owner of the
              journal the comment is posted to suffices.
        Raises a VLEProgramming error when misused.
        """
        if not isinstance(user, User):
            raise VLEProgrammingError("Expected instance of type User.")

        if user == self.author or user.is_superuser:
            return True

        return user.has_permission('can_edit_staff_comment', self.entry.node.journal.assignment) and \
            self.author != self.entry.node.journal.user

    def save(self, *args, **kwargs):
        if not self.pk:
            self.creation_date = timezone.now()
        self.last_edited = timezone.now()
        self.text = sanitization.strip_script_tags(self.text)
        return super(Comment, self).save(*args, **kwargs)

    def to_string(self, user=None):
        return "Comment"
