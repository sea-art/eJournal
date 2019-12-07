"""
entry.py.

In this file are all the entry api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.serializers as serialize
import VLE.tasks.lti as lti_tasks
import VLE.timeline as timeline
import VLE.utils.entry_utils as entry_utils
import VLE.utils.file_handling as file_handling
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
from VLE.models import Entry, Field, Journal, Node, Template


class EntryView(viewsets.ViewSet):
    """Entry view.

    This class creates the following api paths:
    POST /entries/ -- create a new entry
    PATCH /entries/<pk> -- partially update an entry
    """

    def create(self, request):
        """Create a new entry.

        Deletes remaining temporary user files if successful.

        Arguments:
        request -- the request that was send with
            journal_id -- the journal id
            template_id -- the template id to create the entry with
            node_id -- optional: the node to bind the entry to (only for entrydeadlines)
            content -- the list of {tag, data} tuples to bind data to a template field.
        """
        journal_id, template_id, content_list = utils.required_params(
            request.data, "journal_id", "template_id", "content")
        node_id, = utils.optional_params(request.data, "node_id")

        journal = Journal.objects.get(pk=journal_id, authors__user=request.user)
        assignment = journal.assignment
        template = Template.objects.get(pk=template_id)

        request.user.check_permission('can_have_journal', assignment)

        if assignment.is_locked():
            return response.forbidden('The assignment is locked, entries can no longer be edited/changed.')

        if journal.needs_lti_link():
            return response.forbidden(journal.outdated_link_warning_msg)

        # Check if the template is available
        if not (node_id or assignment.format.template_set.filter(archived=False, preset_only=False,
                                                                 pk=template.pk).exists()):
            return response.forbidden('Entry template is not available.')

        entry_utils.check_fields(template, content_list)

        # Node specific entry
        if node_id:
            node = Node.objects.get(pk=node_id, journal=journal)
            entry = entry_utils.add_entry_to_node(node, template, request.user)
        # Template specific entry
        else:
            entry = factory.make_entry(template, request.user)
            node = factory.make_node(journal, entry)

        for content in content_list:
            field_id, = utils.required_typed_params(content, (int, 'id'))
            data, = utils.required_params(content, 'data')
            field = Field.objects.get(pk=field_id)

            created_content = factory.make_content(node.entry, data, field)

            if field.type in field.FILE_TYPES:  # Image, file or PDF
                user_file = file_handling.get_temp_user_file(request.user, assignment, content['data'])
                if user_file is None and field.required:
                    node.entry.delete()
                    # If there is a newly created node, delete that as well
                    if not node_id:
                        node.delete()
                    return response.bad_request('One of your files was not correctly uploaded, please try again.')
                elif user_file:
                    file_handling.make_permanent_file_content(user_file, created_content, node)

        # Notify teacher on new entry
        if node.journal.authors.filter(sourcedid__isnull=False).exists() and \
           node.entry.vle_coupling == Entry.NEED_SUBMISSION:
            lti_tasks.needs_grading.delay(node.pk)

        # Delete old user files
        file_handling.remove_temp_user_files(request.user)

        return response.created({
            'added': entry_utils.get_node_index(journal, node, request.user),
            'nodes': timeline.get_nodes(journal, request.user),
            'entry': serialize.EntrySerializer(entry, context={'user': request.user}).data
        })

    def partial_update(self, request, *args, **kwargs):
        """Update an existing entry.

        Arguments:
        request -- request data
            data -- the new data for the course
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the entry does not exist
            forbidden -- User not allowed to edit this entry
            unauthorized -- when the user is unauthorized to edit the entry
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new entry data

        """
        content_list, = utils.required_typed_params(request.data, (list, 'content'))
        entry_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        entry = Entry.objects.get(pk=entry_id)
        graded = entry.is_graded()
        journal = entry.node.journal
        assignment = journal.assignment

        if assignment.is_locked():
            return response.forbidden('The assignment is locked, entries can no longer be edited/changed.')
        request.user.check_permission('can_have_journal', assignment)
        if not (journal.authors.filter(user=request.user).exists() or request.user.is_superuser):
            return response.forbidden('You are not allowed to edit someone else\'s entry.')
        if graded:
            return response.bad_request('You are not allowed to edit graded entries.')
        if entry.is_locked():
            return response.bad_request('You are not allowed to edit locked entries.')
        if journal.needs_lti_link():
            return response.forbidden(journal.outdated_link_warning_msg)

        # Check for required fields
        entry_utils.check_fields(entry.template, content_list)

        # Attempt to edit the entries content.
        for content in content_list:
            field_id, = utils.required_typed_params(content, (int, 'id'))
            data, = utils.required_params(content, 'data')
            field = Field.objects.get(pk=field_id)

            old_content = entry.content_set.filter(field=field)
            if old_content.exists():
                old_content = old_content.first()
                if old_content.field.pk != field_id:
                    return response.bad_request('The given content does not match the accompanying field type.')
                if not data:
                    old_content.delete()
                    continue

                entry_utils.patch_entry_content(request.user, entry, old_content, field, data, assignment)
            # If there was no content in this field before, create new content with the new data.
            # This can happen with non-required fields, or when the given data is deleted.
            else:
                factory.make_content(entry, data, field)

        file_handling.remove_temp_user_files(request.user)
        entry.last_edited_by = request.user
        entry.save()

        return response.success({'entry': serialize.EntrySerializer(entry, context={'user': request.user}).data})

    def destroy(self, request, *args, **kwargs):
        """Delete an entry and the node it belongs to.

        Arguments:
        request -- request data
        pk -- entry ID

        Returns:
        On failure:
            not found -- when the course does not exist
            unauthorized -- when the user is not logged in
            forbidden -- when the user is not in the course
        On success:
            success -- with a message that the course was deleted
        """
        pk, = utils.required_typed_params(kwargs, (int, 'pk'))

        entry = Entry.objects.get(pk=pk)
        journal = entry.node.journal
        assignment = journal.assignment

        if journal.authors.filter(user=request.user).exists():
            request.user.check_permission('can_have_journal', assignment, 'You are not allowed to delete entries.')
            if entry.is_graded():
                return response.forbidden('You are not allowed to delete graded entries.')
            if entry.is_locked():
                return response.forbidden('You are not allowed to delete locked entries.')
            if assignment.is_locked():
                return response.forbidden('You are not allowed to delete entries in a locked assignment.')
        elif not request.user.is_superuser:
            return response.forbidden('You are not allowed to delete someone else\'s entry.')
        if journal.needs_lti_link():
            return response.forbidden(journal.outdated_link_warning_msg)

        if entry.node.type != Node.ENTRYDEADLINE:
            entry.node.delete()
        entry.delete()
        return response.success(description='Successfully deleted entry.')
