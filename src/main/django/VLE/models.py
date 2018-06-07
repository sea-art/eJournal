from django.db import models


class User(models.Model):
    ADMIN = 'AD'
    TEACHER = 'TE'
    TEACHER_ASSISTANT = 'TA'
    STUDENT = 'SD'
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

    def __str__(self):
        return self.username

    class Meta:
        unique_together = ('username', 'education',)


class Course(models.Model):
    name = models.TextField()
    author = models.ManyToManyField(User)
    abbreviation = models.TextField(max_length=3)
    startdate = models.DateField()

    def __str__(self):
        return self.name


class Assignment(models.Model):
    name = models.TextField()
    description = models.TextField(
        null=True,
    )
    course = models.ManyToManyField(Course)

    def __str__(self):
        return self.name


class Journal(models.Model):
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
    journal = models.ForeignKey(
        'Journal',
        on_delete=models.CASCADE
    )
    datatime = models.DateTimeField(
        auto_now_add=True
    )
    late = models.BooleanField()

    def __str__(self):
        return "Entry: " + str(self.pk)
