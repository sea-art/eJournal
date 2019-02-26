import factory


class InstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Instance'

    name = factory.Sequence(lambda x: 'A' + str(x))
