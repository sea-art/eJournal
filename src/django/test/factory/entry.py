import factory


class EntryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'VLE.Entry'

    node = factory.SubFactory('test.factory.node.NodeFactory')
    template = None
    grade = None
    published = True

    @factory.post_generation
    def add_node(self, create, extracted):
        if not create:
            return

        self.node.entry = self
        self.node.type = 'entry'
        self.node.save()
        self.node.journal.node_set.add(self.node)
