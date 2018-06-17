# Database file
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    User is an entity in the database with the following features:
    - email: email of the user.
    - USERNAME_FIELD: username of the username.
    - password: the hash of the password of the user.
    - lti_id: the DLO id of the user.
    """
    email = models.EmailField(
        null=True,
        blank=True,
        unique=True,
    )
    lti_id = models.TextField(
        null=True,
        unique=True,
    )

    def __str__(self):
        return self.username


class Course(models.Model):
    """
    A Course entity has the following features:
    - name: name of the course.
    - author: the creator of the course.
    - abbrevation: a max three letter abbrevation of the course name.
    - startdate: the date that the course starts.
    """
    name = models.TextField()
    abbreviation = models.TextField(
        max_length=4,
        default='XXXX',
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True
    )
    participations = models.ManyToManyField(
        User,
        related_name='participations',
        through='Participation',
        through_fields=('course', 'user'),
    )

    startdate = models.DateField(
        null=True,
    )

    def __str__(self):
        return self.name


class Role(models.Model):
    """
    A role defines the permissions of a user group within a course.
    - name: name of the role
    - list of permissions (can_...)
    """
    name = models.TextField()

    can_edit_grades = models.BooleanField(default=False)
    can_view_grades = models.BooleanField(default=False)
    can_edit_assignment = models.BooleanField(default=False)
    can_view_assignment = models.BooleanField(default=False)
    can_submit_assignment = models.BooleanField(default=False)

    def __str__(self):
        return str(vars(self))


class Participation(models.Model):
    """
    A participation defines the way a user interacts within a certain course.
    The user is now linked to the course, and has a set of permissions
    associated with it's role.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    role = models.ForeignKey(
        Role,
        null=True,
        on_delete=models.SET_NULL,
        related_name='role',
    )

    # TODO: Unique, but fails in test script.
    # class Meta:
    #     unique_together = ('user', 'course',)


class Assignment(models.Model):
    """
    An Assignment entity has the following features:
    - name: name of the assignment.
    - description: description for the assignment.
    - courses: a foreign key linked to the courses this assignment
    is part of.
    """
    name = models.TextField()
    deadline = models.DateTimeField(
        auto_now_add=True
    )
    description = models.TextField(
        null=True,
    )
    author = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True
    )
    courses = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Journal(models.Model):
    """
    A journal contains the following features:
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

    def __str__(self):
        return self.assignment.name + " from " + self.user.username

    class Meta:
        """
        A class for meta data.
        - unique_together: assignment and user must be unique together.
        """
        unique_together = ('assignment', 'user',)


class Entry(models.Model):
    """
    An Entry has the following features:
    - journal: a foreign key linked to an Journal.
    - datetime: the date and time when the entry was posted.
    - late: if the entry was posted late or not.
    """
    journal = models.ForeignKey(
        'Journal',
        on_delete=models.CASCADE,
    )
    datetime = models.DateTimeField(
        auto_now_add=True,
    )
    late = models.BooleanField(
        default=False
    )
    graded = models.BooleanField(
        default=False
    )

    def __str__(self):
        return str(self.pk)
