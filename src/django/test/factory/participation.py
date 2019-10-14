import factory

import VLE.models


class ParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Participation'

    user = factory.SubFactory('test.factory.user.UserFactory')
    course = factory.SubFactory('test.factory.course.CourseFactory')
    role = factory.SubFactory('test.factory.role.RoleFactory', course=factory.SelfAttribute('..course'))

    @factory.post_generation
    def journals(self, create, extracted):
        if not create:
            return

        for assignment in VLE.models.Assignment.objects.filter(courses__in=[self.course]):
            VLE.models.Journal.objects.create(user=self.user, assignment=assignment)


class GroupParticipationFactory(ParticipationFactory):
    group = factory.SubFactory('test.factory.group.GroupFactory')


class AssignmentParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.AssignmentParticipation'

    user = factory.SubFactory('test.factory.user.UserFactory')
    assignment = factory.SubFactory('test.factory.assignment.AssignmentFactory')
    journal = factory.SubFactory('test.factory.journal.JournalFactory', assignment=factory.SelfAttribute('..assignment'))
