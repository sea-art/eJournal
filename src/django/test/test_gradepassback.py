"""
test_gradepassback.py.

Test the lti grade passback.
"""
from VLE.lti_grade_passback import GradePassBackRequest, needs_grading, replace_result
from django.http import HttpResponse
from django.conf import settings
from django.test import LiveServerTestCase
from django.test.utils import override_settings
from django.urls import path
import VLE.factory as factory


def grade_passback_answer():
    return HttpResponse(b'<?xml version="1.0" encoding="UTF-8"?>\n<imsx_POXEnvelopeResponse xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\n        <imsx_POXHeader>\n          <imsx_POXResponseHeaderInfo>\n            <imsx_version>V1.0</imsx_version>\n            <imsx_messageIdentifier/>\n            <imsx_statusInfo>\n              <imsx_codeMajor>success</imsx_codeMajor>\n              <imsx_severity>status</imsx_severity>\n              <imsx_description/>\n              <imsx_messageRefIdentifier>2</imsx_messageRefIdentifier>\n              <imsx_operationRefIdentifier>replaceResult</imsx_operationRefIdentifier>\n            </imsx_statusInfo>\n          </imsx_POXResponseHeaderInfo>\n        </imsx_POXHeader>\n        <imsx_POXBody><replaceResultResponse/></imsx_POXBody>\n      </imsx_POXEnvelopeResponse>\n')


urlpatterns = [
    path('grade_passback', grade_passback_answer, name='grade_passback_answer'),
]


@override_settings(ROOT_URLCONF=__name__)
class GradePassBackRequestXMLTest(LiveServerTestCase):
    """Test XML grade passpack.

    Test if the gradepassback XML can be created.
    """

    def setUp(self):
        """Setup."""
        self.course = factory.make_course('TestCourse', 'aaaa', lti_id='asdf')
        self.assignment = factory.make_assignment("TestAss", "TestDescr", points_possible=100, courses=[self.course])
        self.user = factory.make_user('TestUser', 'Pass', 'ltiTest@test.com')
        self.journal = factory.make_journal(self.assignment, self.user)
        self.journal.sourcedid = 'f6d552'
        self.journal.grade_url = 'http://127.0.0.1:8000/grade_passback'

    def test_create_grade_passback(self):
        """Test if the GradePassBackRequest is correctly created when a journal is given"""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal, send_score=True)
        self.assertIsNotNone(passback.score)
        self.assertIsNotNone(passback.url)
        self.assertIsNotNone(passback.sourcedid)

    def test_create_grade_passback_no_journal(self):
        """Test if the GradePassBackRequest is correctly created when no journal is given"""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)
        self.assertIsNone(passback.score)
        self.assertIsNone(passback.url)
        self.assertIsNone(passback.sourcedid)

    def test_create_xml_no_score_no_data(self):
        """Test create xml with no score or data set."""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None)
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version>\
<imsx_messageIdentifier>0</imsx_messageIdentifier></imsx_POXRequestHeaderInfo>\
</imsx_POXHeader><imsx_POXBody><replaceResultRequest><resultRecord><sourcedGUID><sourcedId />\
</sourcedGUID></resultRecord></replaceResultRequest></imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.assertEqual(result, passback.create_xml())

    def test_create_xml_with_score(self):
        """Test create xml with the score set."""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal, send_score=True)
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultScore><language>en</language>\
<textString>0.0</textString></resultScore></result></resultRecord></replaceResultRequest></imsx_POXBody>\
</imsx_POXEnvelopeRequest>'

        self.assertEqual(result, passback.create_xml())

    def test_create_xml_with_data_text(self):
        """Test create xml."""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                        result_data={'text': 'New entry'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<text>New entry</text></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.assertEqual(result, passback.create_xml())

    def test_create_xml_with_data_url(self):
        """Test create xml."""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                        result_data={'url': 'http://127.0.0.1:8000/grade_passback'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<url>http://127.0.0.1:8000/grade_passback</url></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.assertEqual(result, passback.create_xml())

    def test_create_xml_with_data_launchUrl(self):
        """Test create xml."""
        passback = GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                        result_data={'launchUrl': 'http://127.0.0.1:8000/grade_passback'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<ltiLaunchUrl>http://127.0.0.1:8000/grade_passback</ltiLaunchUrl></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        self.assertEqual(result, passback.create_xml())

    def test_message_id_incrementor(self):
        """Test if the ID incrementor is implemented."""
        now = GradePassBackRequest.get_message_id_and_increment()
        self.assertTrue(int(now) + 1 == int(GradePassBackRequest.get_message_id_and_increment()))

    # def test_replace_result(self):
    #     """"""
    #     print(replace_result(self.journal))
    #
    # def test_needs_grading(self):
    #     """"""
    #     print(needs_grading(self.journal, 0))
