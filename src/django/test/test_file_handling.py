import os
import test.factory as factory
from pathlib import Path
from test.utils import api

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

# from VLE.views import UserView
from VLE.factory import make_user_file
from VLE.models import UserFile, Field, FileContext
from VLE.utils.file_handling import get_path

BOUNDARY = 'BoUnDaRyStRiNg'
MULTIPART_CONTENT = 'multipart/form-data; boundary=%s' % BOUNDARY


class FileHandlingTest(TestCase):
    def setUp(self):
        self.student = factory.Student()
        self.journal = factory.Journal(user=self.student)
        self.assignment = self.journal.assignment
        self.format = self.journal.assignment.format
        self.teacher = self.journal.assignment.courses.first().author
        self.unrelated_assignment = factory.Assignment()
        self.video = SimpleUploadedFile('file.mp4', b'file_content', content_type='video/mp4')
        self.image = SimpleUploadedFile('file.png', b'image_content', content_type='image/png')
        self.template = factory.TemplateAllTypes(format=self.format)
        self.img_field = Field.objects.get(type=Field.IMG)
        self.rt_field = Field.objects.get(type=Field.RICH_TEXT)
        self.file_field = Field.objects.get(type=Field.FILE)

        self.create_params = {
            'journal_id': self.journal.pk,
            'template_id': self.template.pk,
            'content': []
        }

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

    def test_remove_unused_files(self):
        # Test uploading two files, then post entry, 1 gets removed
        content_fake = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        content_real = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        post = self.create_params
        post['content'] = [{'data': content_real, 'id': self.img_field.pk}]
        entry = api.post(self, 'entries', params=post, user=self.student, status=201)
        assert self.student.filecontext_set.filter(pk=content_real['id']).exists(), 'real file should stay'
        assert not self.student.filecontext_set.filter(pk=content_fake['id']).exists(), 'fake file should be removed'

        # Rich text fields also need to be checked to not be deleted
        content_fake = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        content_real = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        content_rt = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        post = self.create_params
        post['content'] = [
            {'data': content_real, 'id': self.img_field.pk},
            {'data': "<p>hello!<img src='{}' /></p>".format(content_rt['download_url']), 'id': self.rt_field.pk}
        ]
        entry_with_rt = api.post(self, 'entries', params=post, user=self.student, status=201)['entry']
        assert self.student.filecontext_set.filter(pk=content_real['id']).exists(), 'real file should stay'
        assert self.student.filecontext_set.filter(pk=content_rt['id']).exists(), 'rich text shoud stay'
        assert not self.student.filecontext_set.filter(pk=content_fake['id']).exists(), 'fake file should be removed'

        # When file in entry updates, old file needs to be removed
        content_old = content_real
        content_new = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        patch = {
            'pk': entry_with_rt['id'],
            'content': post['content']
        }
        patch['content'][0]['data'] = content_new
        api.update(self, 'entries', params=patch, user=self.student)
        assert self.student.filecontext_set.filter(pk=content_new['id']).exists(), 'new file should exist'
        assert not self.student.filecontext_set.filter(pk=content_old['id']).exists(), 'old file should be removed'

        # When file in rich text updates, old file needs to be removed
        content_old_rt = content_rt
        content_new_rt = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        content_new_rt2 = api.post(
            self, 'files', params={'file': self.image}, user=self.student, content_type=MULTIPART_CONTENT, status=201)
        patch['content'][1]['data'] = "<p>hello!<img src='{}' /><img src='{}' /></p>".format(
            content_new_rt['download_url'], content_new_rt2['download_url'])
        api.update(self, 'entries', params=patch, user=self.student)
        assert self.student.filecontext_set.filter(pk=content_new_rt['id']).exists(), 'new file should exist'
        assert self.student.filecontext_set.filter(pk=content_new_rt2['id']).exists(), 'new file should exist'
        assert not self.student.filecontext_set.filter(pk=content_old_rt['id']).exists(), 'old file should be removed'

    def test_temp_file_upload_student(self):
        api.post(
            self,
            'user/download',
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
