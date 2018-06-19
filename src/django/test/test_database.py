import datetime
import VLE.factory as factory
from django.test import TestCase
from VLE.models import *


class DataBaseTests(TestCase):
    def test_foreignkeys(self):
        """
        Testing the foreign keys in de database.
        """
        user_test = factory.make_user('lers', 'lers123', 'lers@uva.nl', 'a')
        course_test = factory.make_course('tname', 'XXXX', datetime.date.today())
        format = factory.make_journal_format()
        template = factory.make_entry_template("some_template")
        entr_test = factory.make_entry(template)
        field = factory.make_field(template, "test1", "1")
        content = factory.make_content(entr_test, "data", field)
        course_test.author = user_test

        ass_test = factory.make_assignment(name='tcolloq', description='description')
        ass_test.courses.add(course_test)
        journ_test = factory.make_journal(user=user_test, assignment=ass_test)

        self.assertEquals(entr_test.template.pk, template.pk)
        self.assertEquals(journ_test.user.pk, user_test.pk)
        self.assertEquals(journ_test.assignment.pk, ass_test.pk)
        self.assertEquals(course_test.author.pk, user_test.pk)

    def test_cascade(self):
        """
        Testing the cascading relations in the database.
        """
        u1 = factory.make_user("Zi", "pass")
        a1 = factory.make_assignment('tcolloq', 'description')
        et1 = factory.make_entry_template('temp1')
        et2 = factory.make_entry_template('temp2')
        jf1 = factory.make_journal_format()
        jf2 = factory.make_journal_format()

        jf1.available_templates.add()
        jf2.available_templates.add()

        d1 = factory.make_deadline()
        d2 = factory.make_deadline()

        f1 = factory.make_field(et1, "test1", "1")
        f2 = factory.make_field(et1, "test2", "2")
        f3 = factory.make_field(et1, "test3", "3")
        f4 = factory.make_field(et1, "test4", "4")
        f5 = factory.make_field(et2, "test1", "1")
        f6 = factory.make_field(et2, "test2", "2")
        f7 = factory.make_field(et2, "test3", "3")

        j1 = factory.make_journal(a1, u1)

        e1 = factory.make_entry(et1)
        e2 = factory.make_entry(et2)

        c1 = factory.make_content(e1, "hoi", f1)
        c2 = factory.make_content(e1, "doei", f2)
        c3 = factory.make_content(e2, "hoi", f5)
        c4 = factory.make_content(e2, "doei", f6)
