"""
test_permissions.py

This file tests whether all permissions behave as required.
"""
import datetime
from django.test import TestCase

import VLE.factory as factory
import VLE.permissions as permissions


class PermissionTests(TestCase):
    """Test the permission system.

    Test whether the permissions behave as required.
    """

    def setUp(self):
        """Setup."""
        self.u1 = factory.make_user("Zi", "pass")

        self.a1 = factory.make_assignment('tcolloq', 'description')

        self.j1 = factory.make_journal(self.a1, self.u1)

        self.usr = factory.make_user('teun', '1234', email='t@t.com', lti_id='zzzz')
        self.crs = factory.make_course('test course please ignore', 'XXXX', startdate=datetime.date.today())

    def test_get_permissions(self):
        """Test a request that doesn't need permissions."""
        role = factory.make_role('Student', self.crs)

        # Connect a participation to a user, course and role.
        factory.make_participation(self.usr, self.crs, role)

        perm = permissions.get_permissions(self.usr, self.crs.id)

        self.assertFalse(perm['can_delete_course'])

    def test_emptyPermissions(self):
        """Test a request that doesn't need permissions."""
        role = factory.make_role('Student', self.crs)

        # Connect a participation to a user, course and role.
        factory.make_participation(self.usr, self.crs, role)

        self.assertTrue(permissions.has_permissions(self.usr, self.crs.id, []))

    def test_permission(self):
        """Test a request that needs a single permission."""
        role = factory.make_role("Student", self.crs, can_delete_assignment=True)

        factory.make_participation(self.usr, self.crs, role)

        self.assertTrue(permissions.has_permissions(self.usr, self.crs.id, ["can_delete_assignment"]))
        self.assertFalse(permissions.has_permissions(self.usr, self.crs.id, ["can_grade_journal"]))

    def test_permission_multiple(self):
        """Test a request that needs multiple permissions."""
        role = factory.make_role("TA", self.crs, can_delete_assignment=True, can_grade_journal=True,
                                 can_add_assignment=True)

        factory.make_participation(self.usr, self.crs, role)

        self.assertTrue(permissions.has_permissions(self.usr, self.crs.id, ["can_grade_journal"]))
        self.assertFalse(permissions.has_permissions(self.usr, self.crs.id,
                                                     ["can_grade_journal", "can_edit_journal"]))

    def test_get_permissions_admin(self):
        """Test if the admin had the right permissions."""
        user = factory.make_user(email='some@other', username='teun2', password='1234', lti_id='a', is_admin=True)
        role = factory.make_role("TA", self.crs, can_delete_assignment=True,
                                 can_grade_journal=True, can_add_assignment=True)

        factory.make_participation(user, self.crs, role)

        perm = permissions.get_permissions(user, self.crs.id)

        self.assertTrue(perm["is_admin"])

    def test_get_permissions_can_add_course(self):
        """Test if the admin had the right permissions."""
        usr = factory.make_user(email='a@other', username='teun2', password='a', lti_id='a', is_teacher=True)
        usr.save()

        perm = permissions.get_permissions(usr)

        self.assertTrue(perm["can_add_course"])

        usr2 = factory.make_user(email='some@other', username='teun3', password='b', lti_id='b', is_teacher=False)
        usr2.save()

        perm = permissions.get_permissions(usr2)

        self.assertFalse(perm["can_add_course"])

    def test_get_permissions_can_edit_institute(self):
        """Test if the admin had the right permissions."""
        usr = factory.make_user(email='a@other', username='teun2', password='a', lti_id='a', is_admin=True)
        usr.save()

        perm = permissions.get_permissions(usr)

        self.assertTrue(perm["can_edit_institute"])

        usr2 = factory.make_user(email='some@other', username='teun3', password='b', lti_id='b', is_admin=False)
        usr2.save()

        perm = permissions.get_permissions(usr2)

        self.assertFalse(perm["can_edit_institute"])

    def test_get_permissions_no_admin(self):
        """Test a request that returns a dictionary of permissions.

        The created user should NOT be provided with the admin permission.
        """
        role = factory.make_role("TA", self.crs, can_delete_assignment=True,
                                 can_grade_journal=True, can_add_assignment=True)

        factory.make_participation(self.usr, self.crs, role)

        perm = permissions.get_permissions(self.usr, self.crs.id)

        self.assertFalse(perm["is_admin"])
