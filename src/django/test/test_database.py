import datetime
import VLE.factory as factory
from django.test import TestCase
from VLE.models import *
from VLE.util import *


class DataBaseTests(TestCase):
    def setUp(self):
        self.u1 = factory.make_user("Zi", "pass")

        self.a1 = factory.make_assignment('tcolloq', 'description')

        self.et1 = factory.make_entry_template('temp1')
        self.et2 = factory.make_entry_template('temp2')

        self.jf1 = factory.make_journal_format()
        self.jf2 = factory.make_journal_format()

        self.d1 = factory.make_deadline()
        self.d2 = factory.make_deadline()

        self.f1 = factory.make_field(self.et1, "test0", "1")
        self.f2 = factory.make_field(self.et1, "test2", "2")
        self.f3 = factory.make_field(self.et2, "test1", "1")

        self.j1 = factory.make_journal(self.a1, self.u1)

        self.e1 = factory.make_entry(self.et1)
        self.e2 = factory.make_entry(self.et2)

        self.c1 = factory.make_content(self.e1, "testcontent1", self.f1)
        self.c2 = factory.make_content(self.e1, "testcontent2", self.f2)
        self.c3 = factory.make_content(self.e2, "testcontent3", self.f3)

        self.jf1.available_templates.add()
        self.jf2.available_templates.add()

    def test_foreignkeys(self):
        """
        Testing the foreign keys in the database.
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

    def test_get_permissions(self):
        """Test a request that doesn't need permissions."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a')
        usr.save()
        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()
        role = Role(name="Student")
        role.save()

        # Connect a participation to a user, course and role.
        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        perm = get_permissions(usr, crs.id)

        self.assertFalse(perm['can_delete_course'])

    def test_emptyPermissions(self):
        """Test a request that doesn't need permissions."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a')
        usr.save()
        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()
        role = Role(name="Student")
        role.save()

        # Connect a participation to a user, course and role.
        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        self.assertTrue(check_permissions(usr, crs.id, []))

    def test_permission(self):
        """Test a request that needs a single permission."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a')
        usr.save()

        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()

        role = Role(name="Student", can_submit_assignment=True)
        role.save()

        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        self.assertTrue(check_permissions(usr, crs.id, ["can_submit_assignment"]))
        self.assertFalse(check_permissions(usr, crs.id, ["can_edit_grades"]))

    def test_permission_multiple(self):
        """Test a request that needs multiple permissions."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a')
        usr.save()

        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()

        role = Role(name="TA", can_submit_assignment=True, can_view_grades=True, can_edit_assignment=True)
        role.save()

        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        self.assertTrue(check_permissions(usr, crs.id, ["can_view_grades"]))
        self.assertFalse(check_permissions(usr, crs.id, ["can_edit_grades",
                                                         "can_edit_assignment"]))

    def test_get_permissions_admin(self):
        """Test a request that returns a dictionary of permissions. The created
        user should be provided with the admin permission."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a', is_admin=True)
        usr.save()

        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()

        role = Role(name="TA", can_submit_assignment=True, can_view_grades=True, can_edit_assignment=True)
        role.save()

        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        perm = get_permissions(usr, crs.id)

        self.assertTrue(perm["is_admin"])

    def test_get_permissions_no_admin(self):
        """Test a request that returns a dictionary of permissions. The created
        user should NOT be provided with the admin permission."""
        usr = User(email='t@t.com', username='teun',
                   password='1234', lti_id='a', is_admin=False)
        usr.save()

        crs = Course(name='test course please ignore', abbreviation='XXXX',
                     startdate=datetime.date.today())
        crs.save()

        role = Role(name="TA", can_submit_assignment=True, can_view_grades=True, can_edit_assignment=True)
        role.save()

        participation = Participation(user=usr, role=role, course=crs)
        participation.save()

        perm = get_permissions(usr, crs.id)

        self.assertFalse(perm["is_admin"])

    def test_on_delete(self):
        """
        Testing the on_delete relations in the database.
        """
        self.f1.delete()
        self.assertEquals(Field.objects.filter(title='test0').count(), 0)
        self.assertEquals(Content.objects.get(pk=1).field, None)

        self.et1.delete()
        self.et2.delete()

        self.assertEquals(Field.objects.all().count(), 0)

        self.e1.delete()

        self.assertEquals(Content.objects.filter(data='testcontent1').count(), 0)
        self.assertEquals(Content.objects.filter(data='testcontent2').count(), 0)

        self.u1.delete()

        self.assertEquals(Content.objects.all().count(), 1)
        self.assertEquals(Entry.objects.all().count(), 1)
        self.assertEquals(Journal.objects.all().count(), 0)
