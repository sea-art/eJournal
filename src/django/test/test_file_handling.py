import os
import test.factory as factory
from pathlib import Path
from test.utils import api

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

# from VLE.views import UserView
from VLE.factory import make_user_file
from VLE.models import UserFile
from VLE.utils.file_handling import get_path

BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY


class FileHandlingTest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        ap = factory.AssignmentParticipation(user=self.student)
        self.journal = ap.journal
        self.teacher = self.journal.assignment.courses.first().author
        self.unrelated_assignment = factory.Assignment()
        self.video = SimpleUploadedFile('file.mp4', b'file_content', content_type='video/mp4')
        self.student_download_url = reverse('VLE:user-download', kwargs={'pk': self.student.pk})
        self.upload_url = reverse('VLE:user-upload')

    def tearDown(self):
        """Cleans any remaining user_files on the file system (remnants from failed tests) assumes user_file instance
        infact deletes corresponding files"""
        UserFile.objects.filter(author=self.student).delete()
        UserFile.objects.filter(author=self.teacher).delete()

    def test_user_file_model(self):
        user_file = UserFile.objects.filter(author=self.student.pk, file_name=self.video.name)
        assert not user_file.exists(), "Assumes the student has no apriori user files."

        user_file = make_user_file(self.video, self.student, self.journal.assignment)

        user_file_get = UserFile.objects.get(author=self.student.pk, file_name=self.video.name)
        assert user_file, "The student should have succesfully created a temp user file."
        assert user_file == user_file_get, "The created user file should be equal to the gotten user file from db."
        user_file_file_path = user_file.file.path
        actual_file_name = Path(user_file_file_path).name

        assert os.path.exists(user_file_file_path) and os.path.isfile(user_file_file_path), \
            "The file should be created on file styem as an actual file."

        assert actual_file_name == user_file.file_name, "The user file name field should match the actual file name."

        assert get_path(user_file, user_file.file_name) in user_file.file.path, \
            "The user file's file path should follow the get_path logic"

        user_file.delete()
        assert not UserFile.objects.filter(author=self.student.pk, file_name=self.video.name).exists(), \
            "User file should be deleted from DB."
        assert not os.path.exists(user_file_file_path), \
            "Deleting a user file instance should delete the corresponding file as well."

    def test_temp_file_upload_student(self):
        api.post(
            self,
            self.upload_url,
            params={
                'file': self.video,
                'assignment_id': self.journal.assignment.pk,
                'content_id': 'null'
            },
            user=self.student,
            status=200,
            content_type=MULTIPART_CONTENT,
        )
        user_file = UserFile.objects.get(author=self.student.pk, file_name=self.video.name)
        assert user_file, "The student should have succesfully created a temp user file."

        # Cleanup
        user_file.delete()

    def test_temp_file_upload_teacher(self):
        api.post(
            self,
            self.upload_url,
            params={
                'file': self.video,
                'assignment_id': self.journal.assignment.pk,
                'content_id': 'null'
            },
            user=self.teacher,
            status=200,
            content_type=MULTIPART_CONTENT,
        )
        user_file = UserFile.objects.get(author=self.teacher.pk, file_name=self.video.name)
        assert user_file, "The teacher should have succesfully created a temp user file."

        # Cleanup
        user_file.delete()

    def test_student_cant_upload_temp_file_to_unrelated_assignment(self):
        api.post(
            self,
            self.upload_url,
            params={
                'file': self.video,
                'assignment_id': self.unrelated_assignment.pk,
                'content_id': 'null'
            },
            user=self.student,
            status=403,
            content_type=MULTIPART_CONTENT,
        )

    def test_file_upload_needs_actual_file(self):
        response = api.post(
            self,
            self.upload_url,
            params={
                'file': 'not an actual file',
                'assignment_id': self.journal.assignment.pk,
                'content_id': 'null'
            },
            user=self.student,
            status=400,
            content_type=MULTIPART_CONTENT,
        )
        assert "No accompanying file found in the request." in response['description']
