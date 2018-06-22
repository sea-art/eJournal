"""
test_edag.py.

Test all about the edag.
"""
from django.test import TestCase
import datetime

from VLE.models import Deadline, EntryTemplate

import VLE.factory as factory
import VLE.edag as edag


class EdagTests(TestCase):
    """Test the edag."""

    def setUp(self):
        """Setup."""
        self.u_rick = factory.make_user("Rick", "pass")
        self.u_lars = factory.make_user("Lars", "pass")

        self.template = EntryTemplate(name="some_template")
        self.template.save()

        deadline_first = Deadline(datetime=datetime.date(2020, 1, 1))
        deadline_first.save()

        deadline_last_progress = Deadline(datetime=datetime.date(2024, 1, 1), points=10)
        deadline_last_progress.save()

        f_colloq = factory.make_format()
        self.deadlineentry = factory.make_entrydeadline_node(f_colloq, deadline_first, self.template)
        self.progressnode = factory.make_progress_node(f_colloq, deadline_last_progress)
        f_log = factory.make_format()

        a_colloq = factory.make_assignment("Colloq", "In de opdracht...1", author=self.u_rick, format=f_colloq)
        a_log = factory.make_assignment("Logboek", "In de opdracht...2", author=self.u_rick, format=f_log)

        self.j_rick_colloq = factory.make_journal(a_colloq, self.u_rick)
        self.j_lars_colloq = factory.make_journal(a_colloq, self.u_lars)
        self.j_rick_log = factory.make_journal(a_log, self.u_rick)

    def test_deadline_format(self):
        """Test if the deadline is correctly formatted."""
        deadline = Deadline(datetime=datetime.date.today())
        deadline.save()

        format = factory.make_format()
        format.save()
        preset = factory.make_entrydeadline_node(format, deadline, self.template)

        self.assertEquals(deadline, preset.deadline)

        assignment = factory.make_assignment("Portfolio", "Fixed deadlines", author=self.u_rick, format=format)
        journal = factory.make_journal(assignment, self.u_rick)

        self.assertTrue(journal.node_set.get(preset__deadline=deadline))

    def test_sorted(self):
        """Test is the sort function works."""
        entry = factory.make_entry(self.template, datetime.date(2022, 1, 1))
        node = factory.make_node(self.j_rick_colloq, entry)
        nodes = edag.get_sorted_nodes(self.j_rick_colloq)

        self.assertEquals(nodes[0].preset, self.deadlineentry)
        self.assertEquals(nodes[1], node)
        self.assertEquals(nodes[2].preset, self.progressnode)

    def test_json(self):
        """Test is the to dict function works correctly."""
        entry = factory.make_entry(self.template, datetime.date(2022, 1, 1))
        factory.make_node(self.j_rick_colloq, entry)

        nodes = edag.get_nodes_dict(self.j_rick_colloq)

        self.assertEquals(len(nodes), 4)

        self.assertEquals(nodes[0]['type'], 'd')
        self.assertEquals(nodes[0]['entry'], None)
        self.assertEquals(nodes[0]['deadline'], '01-01-2020 00:00')

        self.assertEquals(nodes[1]['type'], 'e')
        self.assertEquals(nodes[1]['entry']['createdate'], '01-01-2022 00:00')

        self.assertEquals(nodes[2]['type'], 'a')

        self.assertEquals(nodes[3]['type'], 'p')
        self.assertEquals(nodes[3]['deadline'], '01-01-2024 00:00')
        self.assertEquals(nodes[3]['target'], 10)
