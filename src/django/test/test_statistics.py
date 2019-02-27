"""
test_statistics.py.

Test the authentication calls.
"""

import test.factory as factory

from django.test import TestCase

import VLE.utils.generic_utils as utils


class StatisticsTests(TestCase):
    """Test statistics functions."""
    def setUp(self):
        """Set up the test file."""
        self.journal = factory.Journal()
        self.entries = [factory.Entry(node__journal=self.journal) for _ in range(4)]

    def test_journal_stats(self):
        """Test the journal stats functions in the serializer."""
        entries = utils.get_journal_entries(self.journal)
        for i in range(len(entries)):
            if i > 0:
                entries[i].grade = 1
                entries[i].published = True
                entries[i].save()
        assert self.journal.get_grade() == 3
        self.journal.bonus_points = 5
        self.journal.save()
        assert self.journal.get_grade() == 8
        assert utils.get_submitted_count(entries) == 4
        assert utils.get_graded_count(entries) == 3
