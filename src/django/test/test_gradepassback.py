from VLE.lti_grade_passback import GradePassBackRequest
from django.conf import settings
from django.test import TestCase
import json


class GradePassBackRequestXMLTest(TestCase):
    """
    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)
        passback.create_xml()
