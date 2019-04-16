import test.factory.user

import factory

import VLE.models


class JournalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Journal'

    assignment = factory.SubFactory('test.factory.assignment.AssignmentFactory')

    @factory.post_generation
    def authors(self, create, extracted):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.authors.add(author)
        else:
            author = test.factory.user.UserFactory()
            self.authors.add(author)

    @factory.post_generation
    def add_user_to_assignment(self, create, extracted):
        for author in self.authors.all():
            for course in self.assignment.courses.all():
                if not VLE.models.Participation.objects.filter(course=course, user=author).exists():
                    role = VLE.models.Role.objects.get(course=course, name='Student')
                    VLE.models.Participation.objects.create(course=course, user=author, role=role)
