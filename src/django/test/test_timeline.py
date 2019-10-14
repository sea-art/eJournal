"""
test_timeline.py.

Test all about the timeline.
"""
import datetime

from django.test import TestCase

import VLE.factory as factory
import VLE.timeline as timeline
from VLE.models import Role
from VLE.utils import generic_utils as utils


class TimelineTests(TestCase):
    """Test the timeline."""

    def setUp(self):
        """Setup."""
        self.u_rick = factory.make_user("Rick", "pass", "r@r.com", full_name='Test User')
        self.u_lars = factory.make_user("Lars", "pass", "l@l.com", full_name='Test User')

        f_colloq = factory.make_default_format()
        self.deadlineentry = factory.make_entrydeadline_node(
            f_colloq, due_date=datetime.datetime.now() - datetime.timedelta(days=10),
            template=f_colloq.template_set.first())
        self.progressnode = factory.make_progress_node(
            f_colloq, datetime.datetime.now() + datetime.timedelta(days=10), 10)
        f_log = factory.make_default_format()

        self.template = f_colloq.template_set.first()

        course = factory.make_course("Some Course", "c")
        student_role = Role.objects.get(name='Student', course=course)
        factory.make_participation(self.u_rick, course, student_role)

        a_colloq = factory.make_assignment("Colloq", "In de opdracht...1",
                                           author=self.u_rick, format=f_colloq, courses=[course])
        a_log = factory.make_assignment("Logboek", "In de opdracht...2",
                                        author=self.u_rick, format=f_log, courses=[course])

        self.j_rick_colloq = factory.make_journal(a_colloq, self.u_rick)
        self.j_lars_colloq = factory.make_journal(a_colloq, self.u_lars)
        self.j_rick_log = factory.make_journal(a_log, self.u_rick)

    def test_due_date_format(self):
        """Test if the due date is correctly formatted."""
        due_date = datetime.date.today()

        format = factory.make_default_format()
        format.save()
        preset = factory.make_entrydeadline_node(format, due_date=due_date,
                                                 template=format.template_set.first())

        self.assertEqual(due_date, preset.due_date)

        assignment = factory.make_assignment("Portfolio", "Fixed deadlines", author=self.u_rick, format=format)
        journal = factory.make_journal(assignment, self.u_rick)

        self.assertTrue(journal.node_set.get(preset__due_date=due_date))

    def test_sorted(self):
        """Test is the sort function works."""
        entry = factory.make_entry(self.template)
        node = factory.make_node(self.j_rick_colloq, entry)
        nodes = utils.get_sorted_nodes(self.j_rick_colloq)

        self.assertEqual(nodes[0].preset, self.deadlineentry)
        self.assertEqual(nodes[1], node)
        self.assertEqual(nodes[2].preset, self.progressnode)

    def test_json(self):
        """Test is the to dict function works correctly."""
        entry = factory.make_entry(self.template)
        factory.make_node(self.j_rick_colloq, entry)

        nodes = timeline.get_nodes(self.j_rick_colloq, self.u_rick)

        self.assertEqual(len(nodes), 4)

        self.assertEqual(nodes[0]['type'], 'd')
        self.assertEqual(nodes[0]['entry'], None)

        self.assertEqual(nodes[1]['type'], 'e')

        self.assertEqual(nodes[2]['type'], 'a')

        self.assertEqual(nodes[3]['type'], 'p')
        self.assertEqual(nodes[3]['target'], 10)
