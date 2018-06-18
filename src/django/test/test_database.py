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
        course_test.author = user_test
        format = JournalFormat()
        format.save()
        ass_test = util.make_assignment(name='tcolloq', description='description')
        ass_test.courses.add(course_test)
        journ_test = util.make_journal(user=user_test, assignment=ass_test)
        entr_test = util.make_entry(journal=journ_test, late=True)
        ass_test = Assignment(name='tcolloq', description='description', format=format)
        ass_test.courses.add(course_test)
        journ_test = Journal(user=user_test, assignment=ass_test)
        journ_test.save()

        template = EntryTemplate(name="some_template")
        template.save()
        entr_test = Entry(datetime=datetime.datetime.today(),
                          late=True,
                          template=template)
        entr_test.save()

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

        jf1.templates.add(et1)
        jf2.template.add(et2)

        d1 = util.make_deadline(jf1)
        d2 = util.make_deadline(jf2)

        f1 = make_field("test1", "1", et1)
        f2 = make_field("test2", "2", et1)
        f3 = make_field("test3", "3", et1)
        f4 = make_field("test4", "4", et1)
        f5 = make_field("test1", "1", et2)
        f6 = make_field("test2", "2", et2)
        f7 = make_field("test3", "3", et2)

        j1 = make_journal(a1, u1)

        e1 = make_entry(j1, et1)
        e2 = make_entry(j1, et2)

        c1 = make_content(e1, "hoi", f1)
        c2 = make_content(e1, "doei", f2)
        c3 = make_content(e2, "hoi", f5)
        c4 = make_content(e2, "doei", f6)
