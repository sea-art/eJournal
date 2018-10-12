"""
test_permissions.py

This file tests whether all permissions behave as required.
"""
import datetime

from django.test import TestCase

import VLE.factory as factory
from VLE.models import Participation, Role


class PermissionTests(TestCase):
    """Test the permission system.

    Test whether the permissions behave as required.
    """

    def setUp(self):
        """Setup."""
        self.u1 = factory.make_user("Zi", "pass", "z@z.com")

        self.a1 = factory.make_assignment('tcolloq', 'description')

        self.j1 = factory.make_journal(self.a1, self.u1)

        self.usr = factory.make_user('teun', '1234', email='t@t.com', lti_id='zzzz')
        self.crs = factory.make_course('test course please ignore', 'XXXX', startdate=datetime.date.today())

    def test_get_permissions(self):
        """Test a request that doesn't need permissions."""
        role = factory.make_role_default_no_perms('SD', self.crs)

        # Connect a participation to a user, course and role.
        factory.make_participation(self.usr, self.crs, role)

        self.assertFalse(self.usr.has_permission('can_delete_course', self.crs))

    def test_permission(self):
        """Test a request that needs a single permission."""
        role = factory.make_role_default_no_perms("SD", self.crs, can_delete_assignment=True)

        factory.make_participation(self.usr, self.crs, role)

        self.assertTrue(self.usr.has_permission('can_delete_assignment', self.crs))
        self.assertFalse(self.usr.has_permission('can_delete_course_user_group', self.crs))

    def test_get_permissions_admin(self):
        """Test if the admin had the right permissions."""
        user = factory.make_user(email='some@other', username='teun2', password='1234',
                                 lti_id='abcde', is_superuser=True)
        role = factory.make_role_default_no_perms("TA1", self.crs, can_delete_assignment=True,
                                                  can_view_assignment_journals=True,
                                                  can_grade=True, can_add_assignment=True)

        factory.make_participation(user, self.crs, role)

        self.assertTrue(user.has_permission('can_edit_institute_details'))

    def test_get_permissions_teacher(self):
        """Test if the admin had the right permissions."""
        usr = factory.make_user(email='some@other', username='teun2', password='1234', lti_id='abcde', is_teacher=True)
        usr.save()

        self.assertTrue(usr.has_permission('can_add_course'))

    def test_get_permissions_no_admin(self):
        """Test a request that returns a dictionary of permissions.

        The created user should NOT be provided with the admin permission.
        """
        role = factory.make_role_default_no_perms("TA1", self.crs, can_delete_assignment=True,
                                                  can_view_assignment_journals=True,
                                                  can_grade=True, can_add_assignment=True)

        factory.make_participation(self.usr, self.crs, role)
        self.assertFalse(self.usr.has_permission('can_edit_institute_details'))

    def test_get_permissions_can_add_course(self):
        """Test whether the admin has the can_add_course permission."""
        usr = factory.make_user(email='a@other', username='teun2', password='a', lti_id='a', is_teacher=True)
        usr.save()
        self.assertTrue(usr.has_permission('can_add_course'))

        usr = factory.make_user(email='b@other', username='teun3', password='b', lti_id='b', is_teacher=False)
        usr.save()
        self.assertFalse(usr.has_permission('can_add_course'))

        usr = factory.make_user(email='c@other', username='teun4', password='b', lti_id='c', is_superuser=True)
        usr.save()
        self.assertTrue(usr.has_permission('can_add_course'))

    def test_get_permissions_can_edit_institute_details(self):
        """Test whether the admin can edit the application institute data."""
        usr = factory.make_user(email='a@other', username='teun2', password='a', lti_id='a', is_superuser=True)
        usr.save()
        self.assertTrue(usr.has_permission('can_edit_institute_details'))

        usr = factory.make_user(email='some@other', username='teun3', password='b', lti_id='b', is_superuser=False)
        usr.save()
        self.assertFalse(usr.has_permission('can_edit_institute_details'))

    def test_get_role(self):
        """Test whether the get_role function returns the right type of value."""
        # Connect a participation to a user, course and role.
        role = factory.make_role_default_no_perms('teststudent2', self.crs)

        factory.make_participation(self.usr, self.crs, role)

        role = Participation.objects.get(user=self.usr, course=self.crs).role
        self.assertTrue(isinstance(role, Role))
