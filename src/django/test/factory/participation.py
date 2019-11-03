import factory

import VLE.factory
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
            VLE.factory.make_journal(user=self.user, assignment=assignment)


class GroupParticipationFactory(ParticipationFactory):
    group = factory.SubFactory('test.factory.group.GroupFactory')
