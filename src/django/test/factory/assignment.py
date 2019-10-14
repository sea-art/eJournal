import datetime
import test.factory.course

import factory
from django.utils import timezone


class AssignmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Assignment'

    name = 'Logboek'
    description = 'Logboek for all your logging purposes'
    is_published = True
    author = factory.SubFactory('test.factory.user.TeacherFactory')
    due_date = timezone.now() + datetime.timedelta(weeks=1)
    lock_date = timezone.now() + datetime.timedelta(weeks=2)

    format = factory.SubFactory('test.factory.format.FormatFactory')

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
            course = test.factory.course.CourseFactory()
            self.courses.add(course)


class TemplateAssignmentFactory(AssignmentFactory):
    class Meta:
        model = 'VLE.Assignment'
    format = factory.SubFactory('test.factory.format.TemplateFormatFactory')


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
    group_size = 3
