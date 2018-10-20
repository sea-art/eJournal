"""
instance.py.

In this file are all the instance api requests.
"""
from rest_framework import viewsets

import VLE.serializers as serialize
import VLE.views.responses as response
import VLE.factory as factory


class InstanceView(viewsets.ViewSet):
    """Instance view.

    This class creates the following api paths:

    """
    def retrieve(self, request, pk):
        """Get a student submitted journal.

        Arguments:
        request -- request data
        pk -- journal ID

        Returns:

        """
        try:
            instance = Instance.objects.get(pk=0)
        except Instance.DoesNotExist:
            factory.make_instance()
            instance = Instance.objects.get(pk=0)

        return response.success({'instance': instance})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing journal.

        Arguments:
        request -- request data
            data -- the new data for the journal
        pk -- journal ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the journal does not exist
            forbidden -- User not allowed to edit this journal
            unauthorized -- when the user is unauthorized to edit the journal
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new journal data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk, = utils.required_typed_params(kwargs, (int, 'pk'))
        journal = Journal.objects.get(pk=pk)

        request.user.check_can_view(journal)

        published, = utils.optional_params(request.data, 'published')
        if published:
            return self.publish(request, journal)

        if not request.user.is_superuser:
            return response.forbidden('You are not allowed to edit this journal.')

        req_data = request.data
        if 'published' in req_data:
            del req_data['published']
        serializer = JournalSerializer(journal, data=req_data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()

        return response.success({'journal': serializer.data})

    def publish(self, request, journal, published=True):
        request.user.check_permission('can_publish_grades', journal.assignment)

        utils.publish_all_journal_grades(journal, published)
        if journal.sourcedid is not None and journal.grade_url is not None:
            payload = lti_grade.replace_result(journal)
        else:
            payload = None

        return response.success({'lti_info': payload})
