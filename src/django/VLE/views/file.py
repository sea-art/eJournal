import re

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

import VLE.utils.responses as response
import VLE.validators as validators
from VLE.models import FileContext


class FileView(viewsets.ViewSet):
    def retrieve(self, request, pk):
        """Get a FileContext file by ID"""
        # TODO FILE implement
        file = FileContext.objects.get(pk=pk)
        return response.file(file, file.file_name)

    def create(self, request):
        if not (request.FILES and 'file' in request.FILES):
            return response.bad_request('No accompanying file found in the request.')

        validators.validate_user_file(request.FILES['file'], request.user)

        file = FileContext.objects.create(
            file=request.FILES['file'],
            file_name=request.FILES['file'].name,
            author=request.user,
            is_temp=True,
        )

        return response.created(
            description='Successfully uploaded {:s}.'.format(request.FILES['file'].name),
            payload={'download_url': file.download_url(access_id=True)}
        )

    @action(['patch'])
    def esteblish(self, request):
        """esteblish files, after this they won't be removed."""
        for file_data in request.data['file_data']:
            name, assignment_id, content_id, course_id, journal_id, = utils.required_params(
                file_data, 'name', 'assignment_id', 'content_id', 'course_id', 'journal_id')
            file = FileContext.objects.get(file_name=name)
            if file.author != request.user:
                return response.forbidden('You are not allowed to update files of other users')
            if not file.is_temp:
                return response.forbidden('You are not allowed to update established files')
            file.assignment = Assignment.objects.get(pk=assignment_id)
            file.content = Content.objects.get(pk=content_id)
            file.course = Course.objects.get(pk=course_id)
            file.journal = Journal.objects.get(pk=journal_id)
            file.is_temp = False
            file.save()

    @action(['get'], detail=True)
    def access_id(self, request, pk):
        """Get a FileContext file by pk"""
        # TODO FILE implement
        file = FileContext.objects.get(access_id=pk)
        return response.file(file, file.file_name)

    # TODO FILE Remove
    def get_permissions(self):
        if re.search(r'^/files/[a-zA-Z0-9]+/access_id/', self.request.path) and self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [permission() for permission in self.permission_classes]
