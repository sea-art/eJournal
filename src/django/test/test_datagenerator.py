from django.core.management import call_command
from django.test import TestCase


class CommandsTestCase(TestCase):
    """Test the self made commands."""

    def setUp(self):
        self.args = []
        self.opts = {}

    def test_presetdb(self):
        """Test preset_db."""
        call_command('preset_db', *self.args, **self.opts)
