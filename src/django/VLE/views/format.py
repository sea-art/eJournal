"""
format.py.

In this file are all the Format api requests.
"""
from rest_framework import viewsets

import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
from VLE.models import Assignment
from VLE.serializers import AssignmentDetailsSerializer, FormatSerializer


class FormatView(viewsets.ViewSet):
    """Format view.

    This class creates the following api paths:
    GET /formats/ -- gets all the formats
    PATCH /formats/<pk> -- partially update an format
    """

    def retrieve(self, request, pk):
        """Get the format attached to an assignment.

        Arguments:
        request -- the request that was sent
        pk -- the assignment id

        Returns a json string containing the format as well as the
        corresponding assignment name and description.
        """
        assignment = Assignment.objects.get(pk=pk)

        request.user.check_can_view(assignment)
        request.user.check_permission('can_edit_assignment', assignment)

        serializer = FormatSerializer(assignment.format)
        assignment_details = AssignmentDetailsSerializer(assignment, context={'user': request.user})

        return response.success({'format': serializer.data, 'assignment_details': assignment_details.data})

    def partial_update(self, request, pk):
        """Update an existing journal format.

        Arguments:
        request -- request data
            templates -- the list of templates to bind to the format
            presets -- the list of presets to bind to the format
            removed_presets -- presets to be removed
            removed_templates -- templates to be removed
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exist
            forbidden -- User not allowed to edit this assignment
            unauthorized -- when the user is unauthorized to edit the assignment
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new assignment data

        """
        assignment_details, templates, presets, removed_templates, removed_presets \
            = utils.required_params(request.data, 'assignment_details', 'templates', 'presets',
                                    'removed_templates', 'removed_presets')

        assignment = Assignment.objects.get(pk=pk)
        format = assignment.format

        request.user.check_permission('can_edit_assignment', assignment)

        # Check if the assignment can be unpublished
        is_published, = utils.optional_params(assignment_details, 'is_published')
        if not assignment.can_unpublish() and is_published is False:
            return response.bad_request("You cannot unpublish an assignment that already has submissions.")

        # Remove data that must not be changed by the serializer
        req_data = assignment_details or {}
        req_data.pop('published', None)
        req_data.pop('author', None)

        for key in req_data:
            if req_data[key] == '':
                req_data[key] = None

        # Update the assignment details
        serializer = AssignmentDetailsSerializer(assignment, data=req_data, context={'user': request.user},
                                                 partial=True)
        if not serializer.is_valid():
            return response.bad_request('Invalid data.')
        serializer.save()

        new_ids = utils.update_templates(format, templates)
        utils.update_presets(assignment, presets, new_ids)

        utils.delete_presets(removed_presets)
        utils.archive_templates(removed_templates)

        serializer = FormatSerializer(format)
        assignment_details = AssignmentDetailsSerializer(assignment, context={'user': request.user})

        return response.success({'format': serializer.data, 'assignment_details': assignment_details.data})
