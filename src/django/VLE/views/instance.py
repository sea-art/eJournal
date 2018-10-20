"""
instance.py.

In this file are all the instance api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.utils.responses as response
from VLE.models import Instance
from VLE.serializers import InstanceSerializer


class InstanceView(viewsets.ViewSet):
    """Instance view.

    This class creates the following api paths:

    """
    def retrieve(self, request, pk=0):
        """Get all instance details."""
        try:
            instance = Instance.objects.get(pk=1)
        except Instance.DoesNotExist:
            instance = factory.make_instance()

        return response.success({'instance': InstanceSerializer(instance).data})

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
        if not request.user.is_superuser:
            return response.forbidden('You are not allowed to edit instance details.')

        try:
            instance = Instance.objects.get(pk=1)
        except Instance.DoesNotExist:
            instance = factory.make_instance()

        req_data = request.data
        serializer = InstanceSerializer(instance, data=req_data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()

        return response.success({'instance': serializer.data})
