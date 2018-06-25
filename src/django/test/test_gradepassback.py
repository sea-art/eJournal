"""
test_gradepassback.py.

Test the grade passback.
"""
from VLE.lti_grade_passback import GradePassBackRequest
from django.conf import settings
from django.test import TestCase


class GradePassBackRequestXMLTest(TestCase):
    """Test XML grade passpack.

    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        """Setup."""
        self.passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)

    def test_create_xml(self):
        """Test create xml."""
        self.passback.create_xml()

    def test_message_id_incrementor(self):
        """Test if the ID incrementor is implemented."""
        now = GradePassBackRequest.get_message_id_and_increment()
        self.assertTrue(int(now) + 1 == int(GradePassBackRequest.get_message_id_and_increment()))
