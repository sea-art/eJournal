import xml.etree.cElementTree as ET

import oauth2
from django.conf import settings

from VLE.models import Counter, Entry


class GradePassBackRequest(object):
    """Class to send Grade replace lti requests."""

    def __init__(self, author, grade, send_score=False, result_data=None, submitted_at=None):
        """
        Create the instance to set the needed variables.

        Arguments:
        key -- key for the oauth communication
        secret -- secret for the oauth communication
        author -- journal author (AssignmentParticipation)
        """
        self.key = settings.LTI_KEY
        self.secret = settings.LTI_SECRET
        self.url = None if author is None else author.grade_url
        self.sourcedid = None if author is None else author.sourcedid
        self.timestamp = submitted_at
        if send_score and author and author.assignment and author.assignment.points_possible:
            score = grade / float(author.assignment.points_possible)
            self.score = str(min(score, 1.0))
        else:
            self.score = None
        self.result_data = result_data

    @classmethod
    def get_message_id_and_increment(cls):
        """Get the current count for message_id and increment this count."""
        try:
            message_id_counter = Counter.objects.get(name='message_id')
        except Counter.DoesNotExist:
            message_id_counter = Counter.objects.create(name='message_id')

        count = message_id_counter.count
        message_id_counter.count += 1
        message_id_counter.save()

        return str(count)

    def create_xml(self):
        """Create the xml used as the body of the lti communication."""
        root = ET.Element(
            'imsx_POXEnvelopeRequest',
            xmlns='http://www.imsglobal.org/services/ltiv1p1/xsd/imsoms_v1p0'
        )
        head = ET.SubElement(root, 'imsx_POXHeader')
        head_info = ET.SubElement(head, 'imsx_POXRequestHeaderInfo')
        imsx_version = ET.SubElement(head_info, 'imsx_version')
        imsx_version.text = 'V1.0'
        msg_id = ET.SubElement(head_info, 'imsx_messageIdentifier')
        msg_id.text = GradePassBackRequest.get_message_id_and_increment()
        body = ET.SubElement(root, 'imsx_POXBody')
        request = ET.SubElement(body, 'replaceResultRequest')

        if self.timestamp is not None:
            submission_details = ET.SubElement(request, 'submissionDetails')
            timestamp = ET.SubElement(submission_details, 'submittedAT')
            timestamp.text = self.timestamp

        result_record = ET.SubElement(request, 'resultRecord')
        sourced_guid = ET.SubElement(result_record, 'sourcedGUID')
        sourced_id = ET.SubElement(sourced_guid, "sourcedId")
        sourced_id.text = self.sourcedid

        if self.score is not None or self.result_data:
            result = ET.SubElement(result_record, 'result')

        if self.score is not None:
            result_score = ET.SubElement(result, 'resultScore')
            language = ET.SubElement(result_score, 'language')
            language.text = 'en'
            score = ET.SubElement(result_score, 'textString')
            score.text = self.score

        if self.result_data:
            data = ET.SubElement(result, 'resultData')
            if 'url' in self.result_data:
                data_url = ET.SubElement(data, 'url')
                data_url.text = self.result_data['url']
            if 'text' in self.result_data:
                data_text = ET.SubElement(data, 'text')
                data_text.text = self.result_data['text']
            if 'launchUrl' in self.result_data:
                launch_url = ET.SubElement(data, 'ltiLaunchUrl')
                launch_url.text = self.result_data['launchUrl']

        return ET.tostring(root, encoding='utf-8')

    def send_post_request(self):
        """
        Send the grade replace post request.

        returns response dictionary with status of request
        """
        if self.url is not None and self.sourcedid is not None:
            consumer = oauth2.Consumer(
                self.key, self.secret
            )
            client = oauth2.Client(consumer)
            _, content = client.request(
                self.url,
                'POST',
                body=self.create_xml(),
                headers={'Content-Type': 'application/xml'}
            )
            return self.parse_return_xml(content)
        return {'severity': 'status',
                'code_mayor': 'No grade passback url set',
                'description': 'not found'}

    def parse_return_xml(self, xml):
        """
        Parse the xml returned by the lti instance.

        Arguments:
        xml -- response xml as byte literal

        returns response dictionary with status of request
        """
        root = ET.fromstring(xml)
        namespace = root.tag.split('}')[0] + '}'
        head = root.find(namespace + 'imsx_POXHeader')
        imsx_head_info = head.find(namespace + 'imsx_POXResponseHeaderInfo')
        imsx_status_info = imsx_head_info.find(namespace + 'imsx_statusInfo')
        imsx_code_mayor = imsx_status_info.find(namespace + 'imsx_codeMajor')
        if imsx_code_mayor is not None and imsx_code_mayor.text is not None:
            code_mayor = imsx_code_mayor.text
        else:
            code_mayor = None

        imsx_severity = imsx_status_info.find(namespace + 'imsx_severity')
        if imsx_severity is not None and imsx_severity.text is not None:
            severity = imsx_severity.text
        else:
            severity = None

        imsx_description = imsx_status_info.find(
            namespace + 'imsx_description')
        if imsx_description is not None and imsx_description.text is not None:
            description = imsx_description.text
        else:
            description = 'not found'

        return {'severity': severity, 'code_mayor': code_mayor,
                'description': description}


def change_entry_vle_coupling(journal, status):
    Entry.objects.filter(grade__published=True, node__journal=journal).exclude(
        vle_coupling=Entry.LINK_COMPLETE).update(vle_coupling=status)


# TODO Move to celery, however order and return is tricky
def replace_result(journal):
    """Replace a grade on the LTI instance based on the request.

    Arguments:
        journal -- the journal of which the grade needs to be updated through lti.

    returns the lti reponse.
    """
    change_entry_vle_coupling(journal, Entry.GRADING)
    response = {}
    failed = False
    for author in journal.authors.all():
        if author.sourcedid is None or author.grade_url is None:
            continue

        grade_request = GradePassBackRequest(author, journal.get_grade(), send_score=True)
        response[author.id] = grade_request.send_post_request()

        if response[author.id]['code_mayor'] != 'success':
            failed = True

    if not failed:
        change_entry_vle_coupling(journal, Entry.LINK_COMPLETE)
    return response if response != {} else None
