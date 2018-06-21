from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    def test_mycommand(self):
        " Test my preset_db and demo_db command."

        args = []
        opts = {}
        call_command('preset_db', *args, **opts)
        call_command('demo_db', *args, **opts)
