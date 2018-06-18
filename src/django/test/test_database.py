import datetime
import VLE.util as util
from django.test import TestCase
from VLE.models import *


class DataBaseTests(TestCase):
    def test_foreignkeys(self):
        """
        Testing the foreign keys in de database.
        """
        user_test = util.make_user('lers', 'lers123', 'lers@uva.nl', 'a')
        course_test = util.make_course('tname', 'XXXX', datetime.date.today())
        format = util.make_journal_format()
        template = util.make_entry_template("some_template")
        entr_test = util.make_entry(template)
        field = util.make_field("test1", "1", template)
        content = util.make_content(entr_test, "data", field)
        course_test.author = user_test

        ass_test = util.make_assignment(name='tcolloq', description='description')
        ass_test.courses.add(course_test)
        journ_test = util.make_journal(user=user_test, assignment=ass_test)

        self.assertEquals(entr_test.template.pk, template.pk)
        self.assertEquals(journ_test.user.pk, user_test.pk)
        self.assertEquals(journ_test.assignment.pk, ass_test.pk)
        self.assertEquals(course_test.author.pk, user_test.pk)

    def test_cascade(self):
        """
        Testing the cascading relations in the database.
        """
        u1 = util.make_user("Zi", "pass")
        a1 = util.make_assignment('tcolloq', 'description')
        et1 = util.make_entry_template('temp1')
        et2 = util.make_entry_template('temp2')
        jf1 = util.make_journal_format()
        jf2 = util.make_journal_format()

        jf1.available_templates.add()
        jf2.available_templates.add()

        d1 = util.make_deadline()
        d2 = util.make_deadline()

        f1 = util.make_field("test1", "1", et1)
        f2 = util.make_field("test2", "2", et1)
        f3 = util.make_field("test3", "3", et1)
        f4 = util.make_field("test4", "4", et1)
        f5 = util.make_field("test1", "1", et2)
        f6 = util.make_field("test2", "2", et2)
        f7 = util.make_field("test3", "3", et2)

        j1 = util.make_journal(a1, u1)

        e1 = util.make_entry(et1)
        e2 = util.make_entry(et2)

        c1 = util.make_content(e1, "hoi", f1)
        c2 = util.make_content(e1, "doei", f2)
        c3 = util.make_content(e2, "hoi", f5)
        c4 = util.make_content(e2, "doei", f6)
