import factory

import VLE.models


class TemplateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Template'

    name = 'default text'

    @factory.post_generation
    def add_fields(self, create, extracted):
        if not create:
            return

        VLE.models.Field.objects.create(type='t', title='title', template=self, location=1, required=True)
        VLE.models.Field.objects.create(type='t', title='summary', template=self, location=2, required=True)
        VLE.models.Field.objects.create(type='t', title='optional', template=self, location=3, required=False)
