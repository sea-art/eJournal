from VLE.lti_launch import *
from django.conf import settings
from django.test import TestCase


class lti_launch_test(TestCase):
    """
    Test if the gradepassback XML can be created.
    """
    def setUp(self):
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)
        passback.create_xml()
