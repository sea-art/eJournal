"""
journalformat.py.

In this file are all the JournalFormat api requests.
"""
from rest_framework import viewsets

from VLE.models import Assignment
import VLE.views.responses as response
import VLE.utils as utils
import VLE.permissions as permissions
import VLE.serializers as serialize


class JournalFormatView(viewsets.ViewSet):
    """Entry view.

    This class creates the following api paths:
    GET /journalformats/ -- gets all the journalformats
    POST /journalformats/ -- create a new journalformat
    GET /journalformats/<pk> -- gets a specific journalformat
    PATCH /journalformats/<pk> -- partially update an journalformat
    DEL /journalformats/<pk> -- delete an journalformat
    """

    def partial_update(self, request, *args, **kwargs):
        """Update an existing journal format.

        Arguments:
        request -- request data
            max_points -- the max points possible.
            templates -- the list of templates to bind to the format
            presets -- the list of presets to bind to the format
            unused_templates -- the list of templates that are bound to the template
                                deck, but are not used in presets nor the entry templates.
            removed_presets -- presets to be removed
            removed_templates -- templates to be removed
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment does not exists
            forbidden -- User not allowed to edit this assignment
            unauthorized -- when the user is unauthorized to edit the assignment
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            aID = kwargs.get('pk')
            templates, presets = utils.required_params(request.data, "templates", "presets")
            unused_templates, max_points = utils.required_params(request.data, "unused_templates", "max_points")
            removed_presets, removed_templates = utils.required_params(request.data, "removed_presets",
                                                                       "removed_templates")

        except KeyError:
            return response.keyerror("aID", "templates", "presets", "unused_templates", "max_points")

        try:
            assignment = Assignment.objects.get(pk=aID)
            format = assignment.format
        except Assignment.DoesNotExist:
            return response.not_found('Assignment')

        if not permissions.has_assignment_permission(request.user, assignment, 'can_edit_assignment'):
            return response.forbidden('You are not allowed to edit this assignment.')

        format.max_points = max_points
        format.save()
        template_map = {}
        utils.update_presets(assignment, presets, template_map)
        utils.update_templates(format.available_templates, templates, template_map)
        utils.update_templates(format.unused_templates, unused_templates, template_map)

        # Swap templates from lists if they occur in the other:
        # If a template was previously unused, but is now used, swap it to available templates, and vice versa.
        utils.swap_templates(format.available_templates, unused_templates, format.unused_templates)
        utils.swap_templates(format.unused_templates, templates, format.available_templates)

        utils.delete_presets(format.presetnode_set, removed_presets)
        utils.delete_templates(format.available_templates, removed_templates)
        utils.delete_templates(format.unused_templates, removed_templates)

        return response.success(payload={'format': serialize.format_to_dict(format)})
