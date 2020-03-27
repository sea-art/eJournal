import datetime
import test.factory.course

import factory
from django.utils import timezone

from VLE.models import Field, Template


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Assignment'

    name = factory.Sequence(lambda x: "Assignment_{}".format(x))
    description = 'Logboek for all your logging purposes'
    is_published = True
    unlock_date = timezone.now()
    due_date = timezone.now() + datetime.timedelta(weeks=1)
    lock_date = timezone.now() + datetime.timedelta(weeks=2)
    is_group_assignment = False
    can_set_journal_name = False
    can_set_journal_image = False
    can_lock_journal = False

    format = factory.SubFactory('test.factory.format.FormatFactory')

    @factory.post_generation
    def courses(self, create, extracted):
        if not create:
            return

        if extracted:
            if self.author is None:
                self.author = extracted[0].author
                self.save()
            for course in extracted:
                self.add_course(course)
                p = factory.SubFactory('test.factory.participation.ParticipationFactory')
                p.user = self.author
                p.course = course
                p.role = factory.SubFactory('test.factory.role.TeacherRoleFactory')
        else:
            course = test.factory.course.CourseFactory()
            self.courses.add(course)

            if self.author is None:
                self.author = self.courses.first().author
                self.save()


class TemplateAssignmentFactory(AssignmentFactory):
    @factory.post_generation
    def add_templates(self, create, extracted):
        if not create:
            return

        template = Template.objects.create(format=self.format, name="template 1 - required summary")
        self.format.template_set.add(template)
        Field.objects.create(type=Field.TEXT, title="Title", location=1, template=template, required=True)
        Field.objects.create(type=Field.RICH_TEXT, title="Summary", location=2, template=template, required=True)
        template = Template.objects.create(format=self.format, name="template 2 - optional summary")
        self.format.template_set.add(template)
        Field.objects.create(type=Field.TEXT, title="Title", location=1, template=template, required=False)
        Field.objects.create(type=Field.RICH_TEXT, title="Summary", location=2, template=template, required=False)


class LtiAssignmentFactory(AssignmentFactory):
    active_lti_id = factory.Sequence(lambda x: "assignment_lti_id{}".format(x))

    @factory.post_generation
    def courses(self, create, extracted):
        if not create:
            return

        if extracted:
            for course in extracted:
                self.courses.add(course)
                p = factory.SubFactory('test.factory.participation.ParticipationFactory')
                p.user = self.author
                p.course = course
                p.role = factory.SubFactory('test.factory.role.TeacherRoleFactory')
        else:
            course = test.factory.course.LtiCourseFactory()
            course.assignment_lti_id_set.append(self.active_lti_id)
            course.save()
            self.courses.add(course)


class GroupAssignmentFactory(AssignmentFactory):
    is_group_assignment = True
    can_lock_journal = True
