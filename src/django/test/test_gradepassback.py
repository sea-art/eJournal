"""
test_gradepassback.py.

Test the lti grade passback.
"""
import test.factory as factory
from test.utils import api

from django.conf import settings
from django.test import TestCase

import VLE.lti_grade_passback as lti_grade
import VLE.tasks.beats.lti as lti_beats
from VLE.models import Entry


class GradePassBackRequestXMLTest(TestCase):
    """Test XML grade passpack.

    Test if the gradepassback XML can be created.

    """
    def setUp(self):
        """Setup."""
        self.student = factory.Student()
        self.teacher = factory.Teacher()
        self.course = factory.LtiCourse(author=self.teacher)
        self.assignment = factory.LtiAssignment(author=self.teacher, courses=[self.course])
        self.journal = factory.Journal(
            assignment=self.assignment, authors=[self.student], sourcedids=['f6d552'],
            grade_url='https://uvadlo-tes.instructure.com/api/lti/v1/tools/267/grade_passback')

    def test_create_grade_passback(self):
        """Test if the GradePassBackRequest is correctly created when a journal is given"""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0], send_score=True)
        assert passback.score
        assert passback.url
        assert passback.sourcedid

    def test_create_grade_passback_no_journal(self):
        """Test if the GradePassBackRequest is correctly created when no journal is given"""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None, None)
        assert passback.score is None
        assert passback.url is None
        assert passback.sourcedid is None

    def test_create_xml_no_score_no_data(self):
        """Test create xml with no score or data set."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, None, None)
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version>\
<imsx_messageIdentifier>0</imsx_messageIdentifier></imsx_POXRequestHeaderInfo>\
</imsx_POXHeader><imsx_POXBody><replaceResultRequest><resultRecord><sourcedGUID><sourcedId />\
</sourcedGUID></resultRecord></replaceResultRequest></imsx_POXBody></imsx_POXEnvelopeRequest>'
        assert result == passback.create_xml()

    def test_create_xml_with_score(self):
        """Test create xml with the score set."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0], send_score=True)
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultScore><language>en</language>\
<textString>0.0</textString></resultScore></result></resultRecord></replaceResultRequest></imsx_POXBody>\
</imsx_POXEnvelopeRequest>'

        assert result == passback.create_xml()

    def test_create_xml_with_data_text(self):
        """Test create xml."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0],
                                                  result_data={'text': 'New entry'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<text>New entry</text></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        assert result == passback.create_xml()

    def test_create_xml_with_data_url(self):
        """Test create xml."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0],
                                                  result_data={'url': 'http://127.0.0.1:8000/grade_passback'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<url>http://127.0.0.1:8000/grade_passback</url></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        assert result == passback.create_xml()

    def test_create_xml_with_data_url_timestamp(self):
        """Test create xml."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0],
                                                  submitted_at='2017-04-16T18:54:36.736+00:00',
                                                  result_data={'url': 'http://127.0.0.1:8000/grade_passback'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<submissionDetails><submittedAT>2017-04-16T18:54:36.736+00:00</submittedAT></submissionDetails>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<url>http://127.0.0.1:8000/grade_passback</url></resultData></result></resultRecord></replaceResultRequest>\
</imsx_POXBody></imsx_POXEnvelopeRequest>'
        assert result == passback.create_xml()

    def test_create_xml_with_data_launchUrl(self):
        """Test create xml."""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0],
                                                  result_data={'launchUrl': 'http://127.0.0.1:8000/grade_passback'})
        result = b'<imsx_POXEnvelopeRequest xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXRequestHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier>0\
</imsx_messageIdentifier></imsx_POXRequestHeaderInfo></imsx_POXHeader><imsx_POXBody><replaceResultRequest>\
<resultRecord><sourcedGUID><sourcedId>f6d552</sourcedId></sourcedGUID><result><resultData>\
<ltiLaunchUrl>http://127.0.0.1:8000/grade_passback</ltiLaunchUrl></resultData></result></resultRecord>\
</replaceResultRequest></imsx_POXBody></imsx_POXEnvelopeRequest>'
        assert result == passback.create_xml()

    def test_message_id_incrementor(self):
        """Test if the ID incrementor is implemented."""
        now = lti_grade.GradePassBackRequest.get_message_id_and_increment()
        assert int(now) + 1 == int(lti_grade.GradePassBackRequest.get_message_id_and_increment())

    def test_parse_return_xml(self):
        """"""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0])
        xml = b'<?xml version="1.0" encoding="UTF-8"?>\
<imsx_POXEnvelopeResponse xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXResponseHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier/>\
<imsx_statusInfo><imsx_codeMajor>success</imsx_codeMajor><imsx_severity>status</imsx_severity>\
<imsx_description>grade replaced</imsx_description><imsx_messageRefIdentifier>2</imsx_messageRefIdentifier>\
<imsx_operationRefIdentifier>replaceResult</imsx_operationRefIdentifier></imsx_statusInfo>\
</imsx_POXResponseHeaderInfo></imsx_POXHeader><imsx_POXBody>\
<replaceResultResponse/></imsx_POXBody></imsx_POXEnvelopeResponse>'
        data = passback.parse_return_xml(xml)
        assert data['severity'] == 'status'
        assert data['code_mayor'] == 'success'
        assert data['description'] == 'grade replaced'

    def test_parse_return_empty_xml(self):
        """"""
        passback = lti_grade.GradePassBackRequest(settings.LTI_SECRET, settings.LTI_KEY, self.journal,
                                                  self.journal.sourcedids[0])
        xml = b'<?xml version="1.0" encoding="UTF-8"?>\
<imsx_POXEnvelopeResponse xmlns="http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0">\
<imsx_POXHeader><imsx_POXResponseHeaderInfo><imsx_version>V1.0</imsx_version><imsx_messageIdentifier/>\
<imsx_statusInfo><imsx_messageRefIdentifier>2</imsx_messageRefIdentifier>\
<imsx_operationRefIdentifier>replaceResult</imsx_operationRefIdentifier></imsx_statusInfo>\
</imsx_POXResponseHeaderInfo></imsx_POXHeader><imsx_POXBody>\
<replaceResultResponse/></imsx_POXBody></imsx_POXEnvelopeResponse>'
        data = passback.parse_return_xml(xml)
        assert data['severity'] is None
        assert data['code_mayor'] is None
        assert data['description'] == 'not found'

    def test_check_if_need_VLE_publish_no_journals(self):
        """Hopefully doesnt crash."""
        course = factory.LtiCourse()
        factory.LtiAssignment(courses=[course])
        lti_beats.check_if_need_VLE_publish()

    def test_check_if_need_VLE_publish_journals_nothing_needed(self):
        """Hopefully doesnt crash."""
        lti_beats.check_if_need_VLE_publish()

    def test_check_if_need_VLE_publish_journals(self):
        """Hopefully doesnt crash."""
        factory.Entry(node__journal=self.journal, vle_coupling=Entry.GRADING)
        factory.Entry(node__journal=self.journal)
        lti_beats.check_if_need_VLE_publish()

    def test_update_journal_entries_vle_state(self):
        """Hopefully doesnt crash."""
        entry = factory.Entry(node__journal=self.journal)
        api.create(self, 'grades', params={'entry_id': entry.id, 'grade': 0, 'published': True},
                   user=self.teacher)
        lti_grade.change_entry_vle_coupling(self.journal, Entry.GRADING)

        entry = Entry.objects.get(pk=entry.pk)
        assert entry.vle_coupling == Entry.GRADING, 'Check if change_entry_vle_coupling works'

    def test_replace_result_no_url(self):
        """Hopefully doesnt crash."""
        entry = factory.Entry(node__journal=self.journal)
        api.create(self, 'grades', params={'entry_id': entry.id, 'grade': 0, 'published': True},
                   user=self.teacher)
        self.journal.sourcedids = None
        self.journal.grade_url = None
        self.journal.save()

        assert lti_grade.replace_result(self.journal) is None
