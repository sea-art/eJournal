from rest_framework import viewsets

import VLE.utils.responses as response


class FileView(viewsets.ViewSet):
    def retrieve(self, request, pk):
        """Get a FileContext file by ID"""
        return response.success("TODO implement")

    def create(self, request):
        return response.succes("TODO implement")
