from rest_framework import viewsets

import VLE.utils.responses as response
import VLE.validators as validators
from VLE.models import FileContext
from rest_framework.permissions import AllowAny
import re


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
            payload={'download_url': file.download_url()}
        )

    def get_permissions(self):
        if re.search(r'^/files/\d+/', self.request.path) and self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [permission() for permission in self.permission_classes]
