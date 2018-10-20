"""
instance.py.

In this file are all the instance api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.serializers as serialize
import VLE.utils.responses as response


class InstanceView(viewsets.ViewSet):
    """Instance view.

    This class creates the following api paths:

    """
    def retrieve(self, request, pk=0):
        """Get all instance details."""
        try:
            instance = Instance.objects.get(pk=0)
        except Instance.DoesNotExist:
            factory.make_instance()
            instance = Instance.objects.get(pk=0)

        return response.success({'instance': instance})

    def partial_update(self, request, *args, **kwargs):
        """Update instance details.

        Arguments:
        request -- request data
            data -- the new data for the journal

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            forbidden -- User not allowed to edit instance
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new instance details
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        if not request.user.is_superuser:
            return response.forbidden('You are not allowed to edit instance details.')

        try:
            instance = Instance.objects.get(pk=0)
        except Instance.DoesNotExist:
            factory.make_instance()
            instance = Instance.objects.get(pk=0)

        req_data = request.data
        serializer = InstanceSerializer(journal, data=req_data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()

        return response.success({'instance': serializer.data})
