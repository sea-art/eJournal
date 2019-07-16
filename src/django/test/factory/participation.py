import factory


class ParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Participation'

    user = factory.SubFactory('test.factory.user.UserFactory')
    course = factory.SubFactory('test.factory.course.CourseFactory')
    role = factory.SubFactory('test.factory.role.RoleFactory', course=factory.SelfAttribute('..course'))


class GroupParticipationFactory(ParticipationFactory):
    group = factory.SubFactory('test.factory.group.GroupFactory')


class AssignmentParticipationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.AssignmentParticipation'

    user = factory.SubFactory('test.factory.user.UserFactory')
    assignment = factory.SubFactory('test.factory.assignment.AssignmentFactory')
    journal = factory.SubFactory('test.factory.journal.JournalFactory', assignment=factory.SelfAttribute('..assignment'))
