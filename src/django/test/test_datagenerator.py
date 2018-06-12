from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    def test_mycommand(self):
        " Test my populate_db command."

        args = []
        opts = {}
        call_command('populate_db', *args, **opts)
