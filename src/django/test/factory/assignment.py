import datetime
import test.factory.course

import factory
from django.utils import timezone

from VLE.models import Template


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Assignment'

    name = 'Logboek'
    description = 'Logboek for all your logging purposes'
    is_published = True
    unlock_date = timezone.now()
    due_date = timezone.now() + datetime.timedelta(weeks=1)
    lock_date = timezone.now() + datetime.timedelta(weeks=2)

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
                self.courses.add(course)
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

        template = Template.objects.create(format=self.format, name="template 1")
        self.format.template_set.add(template)
        template = Template.objects.create(format=self.format, name="template 2")
        self.format.template_set.add(template)


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
