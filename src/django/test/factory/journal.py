import test.factory.participation

import factory

import VLE.factory
import VLE.models


class JournalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Journal'

    assignment = factory.SubFactory('test.factory.assignment.AssignmentFactory')

    @factory.post_generation
    def add_authors(self, create, extracted):
        if not create:
            return

        if extracted:
            for author in extracted:
                if VLE.models.AssignmentParticipation.objects.filter(user=author, assignment=self.assignment).exists():
                    continue
                self.authors.add(VLE.factory.make_assignment_participation(self.assignment, author))
        else:
            print(VLE.models.AssignmentParticipation.objects.filter(journal=self).exists())
            if not VLE.models.AssignmentParticipation.objects.filter(journal=self).exists():
                author = test.factory.participation.AssignmentParticipationFactory(
                    journal=self, assignment=self.assignment)
                self.authors.add(author)

        for author in self.authors.all():
            for course in self.assignment.courses.all():
                if not VLE.models.Participation.objects.filter(course=course, user=author.user).exists():
                    role = VLE.models.Role.objects.get(course=course, name='Student')
                    VLE.models.Participation.objects.create(course=course, user=author.user, role=role)

    @factory.post_generation
    def add_user_to_assignment(self, create, extracted):
        if not create:
            return
        if not VLE.models.AssignmentParticipation.objects.filter(journal=self).exists():
            author = test.factory.participation.AssignmentParticipationFactory(
                journal=self, assignment=self.assignment)
            self.authors.add(author)
        for author in self.authors.all():
            for course in self.assignment.courses.all():
                if not VLE.models.Participation.objects.filter(course=course, user=author.user).exists():
                    role = VLE.models.Role.objects.get(course=course, name='Student')
                    VLE.models.Participation.objects.create(course=course, user=author.user, role=role)


class GroupJournalFactory(JournalFactory):
    assignment = factory.SubFactory('test.factory.assignment.GroupAssignmentFactory')
