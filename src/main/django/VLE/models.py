from django.db import models

class User(models.Model):
    ADMIN = 'AD'
    TEACHER = 'TE'
    TEACHER_ASSISTANT = 'TA'
    STUDENT = 'SU'
    USER_TYPES = (
        (ADMIN, 'Admin'),
        (TEACHER, 'Teacher'),
        (TEACHER_ASSISTANT, 'Teacher assistant'),
        (STUDENT, 'Student'),
    )
    type = models.TextField(
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
    passhash = models.CharField(
        max_length=256,
    )
    education = models.TextField(
        null=True,
    )
    lti_id = models.TextField(
        null=True,
    )

    class Meta:
        unique_together = ('username', 'education',)


class Course(models.Model):
    name = models.TextField()
    author = models.ManyToManyField(User)


class Assignment(models.Model):
    name = models.TextField()
    description = models.TextField(
        null=True,
    )
    course = models.ManyToManyField(Course)


class Journal(models.Model):
    assignment = models.ForeignKey(
        'Assignment',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        'User',
        on_delete=models.CASCADE
    )


class Entry(models.Model):
    journal = models.ForeignKey(
        'Journal',
        on_delete=models.CASCADE
    )
    datatime = models.DateTimeField(
        auto_now_add=True
    )
    late = models.BooleanField()
