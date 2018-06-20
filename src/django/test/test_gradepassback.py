from VLE.lti_grade_passback import GradePassBackRequest
from django.conf import settings
from django.test import TestCase
import json


class GradePassBackRequestXMLTest(TestCase):
    """
    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        self.passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)

    def test_create_xml(self):
        self.passback.create_xml()

    def test_message_id_incrementor(self):
        now = GradePassBackRequest.get_message_id_and_increment()
        self.assertTrue(int(now) + 1 == int(GradePassBackRequest.get_message_id_and_increment()))
