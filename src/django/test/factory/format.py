import factory

import VLE.models


class FormatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Format'


class TemplateFormatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Format'

    assignment = factory.SubFactory('test.factory.assignment.AssignmentFactory')

    @factory.post_generation
    def add_templates(self, create, extracted):
        if not create:
            return

        template = VLE.models.Template.objects.create(format=self, name="template 1")
        self.template_set.add(template)
        template = VLE.models.Template.objects.create(format=self, name="template 2")
        self.template_set.add(template)
