from rest_framework.test import APIRequestFactory
from django.test import TestCase
from django.urls import reverse
import datetime

from VLE.models import User
from VLE.models import Participation
from VLE.models import Role
from VLE.models import Course
from VLE.models import Assignment
from VLE.models import Journal
from VLE.models import Deadline
from VLE.models import EntryTemplate

import VLE.edag as edag
import VLE.util as util


class EdagTests(TestCase):
    def setUp(self):
        self.u_rick = util.make_user("Rick", "pass")
        u_lars = util.make_user("Lars", "pass")

        f_colloq = util.make_format()
        f_log = util.make_format()

        a_colloq = util.make_assignment("Colloq", "In de opdracht...1", self.u_rick, f_colloq)
        a_log = util.make_assignment("Logboek", "In de opdracht...2", self.u_rick, f_log)

        j_rick_colloq = util.make_journal(a_colloq, self.u_rick)
        j_lars_colloq = util.make_journal(a_colloq, u_lars)
        j_rick_log = util.make_journal(a_log, self.u_rick)

    def test_deadline_format(self):
        deadline = Deadline(datetime=datetime.date.today())
        deadline.save()

        format = util.make_format()
        format.save()
        template = EntryTemplate(name="some_template")
        template.save()
        preset = util.make_entrydeadline_node(format, deadline, template)

        self.assertEquals(deadline, preset.deadline)

        assignment = util.make_assignment("Portfolio", "Fixed deadlines", self.u_rick, format)
        journal = util.make_journal(assignment, self.u_rick)

        self.assertTrue(journal.node_set.get(preset__deadline=deadline))
