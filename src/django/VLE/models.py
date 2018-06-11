# Database file
from django.db import models


class User(models.Model):
    """
    User is an entity in the database with the following features:
    - group: the group determines the permissions on the application.
    - email: email of the user.
    - username: username of the username.
    - passhash: the hash of the password of the user.
    - education: the education institute of the userself.
    - lti_id: the DLO id of the user.
    """
    SUPERUSER = 'SU'
    EXAMINATOR = 'EX'
    TEACHER = 'TE'
    TEACHER_ASSISTANT = 'TA'
    STUDENT = 'SD'
    USER_TYPES = (
        (SUPERUSER, 'Super User'),
        (EXAMINATOR, 'Examintor'),
        (TEACHER, 'Teacher'),
        (TEACHER_ASSISTANT, 'Teacher Assistant'),
        (STUDENT, 'Student'),
    )
    group = models.TextField(
        max_length=2,
        choices=USER_TYPES,
        default=STUDENT,
    )
    email = models.TextField(
        unique=True,
        null=True,
    )
    username = models.TextField(
        unique=True,
    )
    password = models.CharField(
        max_length=256,
    )
    education = models.TextField(
        null=True,
    )
    lti_id = models.TextField(
        null=True,
    )

    def __str__(self):
        return self.username

    class Meta:
        """
        A class for meta data.
        - unique_together: username and education must be unique together.
        """
        unique_together = ('username', 'education',)


class Course(models.Model):
    """
    A Course entity has the following features:
    - name: name of the course.
    - author: the creator of the course.
    - abbrevation: a max three letter abbrevation of the course name.
    - startdate: the date that the course starts.
    """
    name = models.TextField()
    author = models.ManyToManyField(User)
    abbreviation = models.TextField(
        max_length=4,
        default='XXXX',
    )
    startdate = models.DateField(
        null=True,
    )

    def __str__(self):
        return self.name


class Assignment(models.Model):
    """
    An Assignment entity has the following features:
    - name: name of the assignment.
    - description: description for the assignment.
    - course: a foreign key linked to a course.
    """
    name = models.TextField()
    description = models.TextField(
        null=True,
    )
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Journal(models.Model):
    """
    A journal contains the following features:
    - assignment: a foreign key linked to an assignment.
    - user: a foreign key linked to an user.
    """
    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.assignment.name + " from " + self.user.username


class Entry(models.Model):
    """
    An Entry has the following features:
    - journal: a foreign key linked to an Journal.
    - datetime: the date and time when the entry was posted.
    - late: if the entry was posted late or not.
    """
    journal = models.ForeignKey(
        'Journal',
        on_delete=models.CASCADE
    )
    datetime = models.DateTimeField(
        auto_now_add=True
    )
    late = models.BooleanField()

    def __str__(self):
        return str(self.pk)
