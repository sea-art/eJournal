from datetime import date

import factory


class GradeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Grade'

    entry = factory.SubFactory('test.factory.entry.EntryFactory')
    grade = 1
    published = True
    date = date(2019, 1, 1)
    author = None

    @factory.post_generation
    def add_author(self, create, extracted):
        if not create:
            return

        self.author = self.entry.node.journal.assignment.courses.first().author
        self.save()
