from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    def setUp(self):
        self.args = []
        self.opts = {}

    def test_presetdb(self):
        " Test preset_db, demo_db and random_db command."
        call_command('preset_db', *self.args, **self.opts)

    def test_demodb(self):
        call_command('demo_db', *self.args, **self.opts)

    def test_reandomdb(self):
        call_command('random_db', *self.args, **self.opts)
