import datetime
from django.test import TestCase
from VLE.models import *
from VLE.util import *


class DataBaseTests(TestCase):
    def test_foreignkeys(self):
        """
        Testing the foreign keys in de database.
        """
        user_test = User(email='lers@uva.nl', username='lers',
                         password='lers123', lti_id='a')
        course_test = Course(name='tname', abbreviation='XXXX',
                             startdate=datetime.date.today())
        user_test.save()
        course_test.save()
        course_test.author = user_test
        ass_test = Assignment(name='tcolloq', description='description')
        ass_test.save()
        ass_test.courses.add(course_test)
        journ_test = Journal(user=user_test, assignment=ass_test)
        journ_test.save()
        entr_test = Entry(journal=journ_test,
                          datetime=datetime.datetime.today(), late=True)
        entr_test.save()

        self.assertEquals(entr_test.journal.pk, journ_test.pk)
        self.assertEquals(journ_test.user.pk, user_test.pk)
        self.assertEquals(journ_test.assignment.pk, ass_test.pk)
        self.assertEquals(course_test.author.pk, user_test.pk)

    def test_getPermissions(self):
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

        perm = get_permissions(usr, crs)

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
