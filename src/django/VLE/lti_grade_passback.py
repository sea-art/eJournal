from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
from rest_framework.decorators import api_view
from django.conf import settings
import oauth2
import json
import xml.etree.cElementTree as ET

from .models import Journal, Counter


class GradePassBackRequest(object):
    # TODO Docstring
    def __init__(self, key, secret, journal):
        self.key = key
        self.secret = secret
        self.url = None  # TODO database url
        self.sourcedId = None  # TODO database sourcedId
        self.score = None  # TODO database
        self.result_data = None

    @classmethod
    def get_message_id_and_increment(cls):
        """
        Get the current count for message_id and increment this count.
        """
        try:
            message_id_counter = Counter.objects.get(name='message_id')
        except Counter.DoesNotExist:
            message_id_counter = Counter.objects.create(name='message_id', count=1)

        count = message_id_counter.count
        message_id_counter.count += 1
        message_id_counter.save()

        return str(count)

    def create_xml(self):
        # TODO Docstring
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
        result_record = ET.SubElement(request, 'resultRecord')
        sourced_guid = ET.SubElement(result_record, 'sourcedGUID')
        sourced_id = ET.SubElement(sourced_guid, "sourcedId")
        sourced_id.text = self.sourcedId

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
            if 'text' in self.result_data:
                data_text = ET.SubElement(data, 'text')
                data_text.text = self.result_data['text']
            if 'url' in self.result_data:
                data_url = ET.SubElement(data, 'url')
                data_url.text = self.result_data['url']
            if 'launchUrl' in self.result_data:
                launch_url = ET.SubElement(data, 'ltiLaunchUrl')
                launch_url.text = self.result_data['launchUrl']

        return ET.tostring(root, encoding='utf-8')

    def send_post_request(self):
        # TODO Docstring
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

    def parse_return_xml(self, content):
        root = ET.fromstring(content)
        namespace = root.tag.split('}')[0]+'}'
        head = root.find(namespace+'imsx_POXHeader')
        print(list(head))
        imsx_head_info = head.find(namespace+'imsx_POXResponseHeaderInfo')
        imsx_status_info = imsx_head_info.find(namespace+'imsx_statusInfo')
        imsx_code_mayor = imsx_status_info.find(namespace+'imsx_codeMajor')
        if imsx_code_mayor is not None:
            code_mayor = imsx_code_mayor.text
        else:
            code_mayor = '???'

        imsx_severity = imsx_status_info.find(namespace+'imsx_severity')
        if imsx_severity is not None:
            severity = imsx_severity.text
        else:
            severity = '???'

        imsx_description = imsx_status_info.find(namespace+'imsx_description')
        if imsx_description is not None and imsx_description.text is not None:
            description = imsx_description.text
        else:
            description = 'not found'

        return {'severity': severity, 'code_mayor': code_mayor, 'description': description}
