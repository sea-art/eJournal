import re

from django.db.models import Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

import VLE.utils.responses as response
import VLE.validators as validators
from VLE.models import FileContext
from VLE.serializers import FileSerializer


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

        return response.created(FileSerializer(file).data)

    @action(['get'], detail=True)
    def access_id(self, request, pk):
        """Get a FileContext file by access_id"""
        file = FileContext.objects.get(access_id=pk)
        return response.file(file, file.file_name)

    # TODO FILE Remove
    def get_permissions(self):
        if re.search(r'^/files/[a-zA-Z0-9]+/access_id/', self.request.path) and self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [permission() for permission in self.permission_classes]
