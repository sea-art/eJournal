"""
entry.py.

In this file are all the entry api requests.
"""
from rest_framework import viewsets
from django.utils.timezone import now
from datetime import datetime

from VLE.models import Journal, Node, Field, Template, Entry, Comment, Content
import VLE.views.responses as response
import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.utils.entry_utils as entry_utils
from VLE.utils import file_handling
import VLE.lti_grade_passback as lti_grade
import VLE.timeline as timeline
import VLE.permissions as permissions
import VLE.serializers as serialize
import VLE.validators as validators


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
        if not request.user.is_authenticated:
            return response.unauthorized()

        journal_id, template_id, content_list = utils.required_params(
            request.data, "journal_id", "template_id", "content")
        node_id, = utils.optional_params(request.data, "node_id")

        journal = Journal.objects.get(pk=journal_id, user=request.user)
        template = Template.objects.get(pk=template_id)

        if node_id:
            node = Node.objects.get(pk=node_id, journal=journal)

            if not (node.preset and node.preset.forced_template == template):
                return response.forbidden('Invalid template for preset node.')
        elif not journal.assignment.format.available_templates.all().filter(pk=template.pk).exists():
            return response.forbidden('Entry template is not available.')

        if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal'):
            return response.forbidden('You are not allowed to create an entry for this journal.')

        if (journal.assignment.unlock_date and journal.assignment.unlock_date > datetime.now()) or \
           (journal.assignment.lock_date and journal.assignment.lock_date < datetime.now()):
            return response.forbidden('The assignment is locked, no entries can be added.')

        # If node id is passed, the entry should be attached to a pre-existing node (entrydeadline node)
        if node_id:
            if node.type != Node.ENTRYDEADLINE:
                return response.bad_request('Passed node is not an EntryDeadline node.')

            if node.entry:
                return response.bad_request('Passed node already contains an entry.')

            if node.preset.deadline < now() or \
               (journal.assignment.due_date and journal.assignment.due_date < datetime.now()):
                return response.bad_request('The deadline has already passed.')

            node.entry = factory.make_entry(template)
            node.save()
        else:
            entry = factory.make_entry(template)
            node = factory.make_node(journal, entry)

        if journal.sourcedid is not None and journal.grade_url is not None:
            lti_grade.needs_grading(journal, node.id)

        for content in content_list:
            data, field_id = utils.required_params(content, 'data', 'id')
            field = Field.objects.get(pk=field_id)
            validators.validate_entry_content(data, field)

            created_content = factory.make_content(node.entry, data, field)

            if field.type in ['i', 'f', 'p']:
                user_file = file_handling.get_temp_user_file(request.user, journal.assignment, content['data'])
                if user_file is None:
                    node.entry.delete()
                    return response.bad_request('One of your files was not correctly uploaded, please try gain.')

                file_handling.make_permanent_file_content(user_file, created_content, node)

        file_handling.remove_temp_user_files(request.user)

        # Find the new index of the new node so that the client can automatically scroll to it.
        result = timeline.get_nodes(journal, request.user)
        added = -1
        for i, result_node in enumerate(result):
            if result_node['nID'] == node.id:
                added = i
                break

        return response.created({
            'added': added,
            'nodes': timeline.get_nodes(journal, request.user)
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
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk = kwargs.get('pk')

        entry = Entry.objects.get(pk=pk)

        grade, published, content_list = utils.optional_params(request.data, "grade", "published", "content")

        journal = entry.node.journal

        if grade and \
           not permissions.has_assignment_permission(request.user, journal.assignment, 'can_grade'):
            return response.forbidden('You cannot grade or publish entries.')
        elif isinstance(grade, (int, float)) and grade < 0:
            return response.bad_request('Grade must be greater or equal to zero.')
        elif grade:
            entry.grade = grade

        if published is not None and \
           not permissions.has_assignment_permission(request.user, journal.assignment, 'can_publish_grades'):
            return response.forbidden('You cannot publish entries.')

        if ((journal.assignment.unlock_date and journal.assignment.unlock_date > datetime.now()) or
            (journal.assignment.lock_date and journal.assignment.lock_date < datetime.now())) and \
           not permissions.has_assignment_permission(request.user, journal.assignment,
                                                     'can_view_assignment_journals'):
            return response.bad_request('The assignment is locked and unavailable for students.')

        if published is not None:
            entry.published = published
            try:
                entry.save()
            except ValueError:
                return response.bad_request('Invalid grade or published state.')
            if published:
                Comment.objects.filter(entry=entry).update(published=True)

        # Attempt to edit the entries content.
        if content_list:
            if not (journal.user == request.user or request.user.is_superuser):
                response.forbidden('You are not allowed to edit someone else\'s entry.')

            if not permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal'):
                return response.forbidden('You are not allowed to have a journal.')

            if entry.grade is not None:
                return response.bad_request('You are not allowed to edit graded entries.')

            if entry.node.type == Node.ENTRYDEADLINE and entry.node.preset.deadline < now() or \
               (journal.assignment.due_date and journal.assignment.due_date < datetime.now()):
                return response.bad_request('You are not allowed to edit entries past their due date.')

            for content in content_list:
                field_id, data, content_id = utils.required_params(content, 'id', 'data', 'contentID')
                field = Field.objects.get(pk=int(field_id))
                old_content = entry.content_set.get(pk=int(content_id))
                validators.validate_entry_content(data, field)

                if old_content.field.pk != int(field_id):
                    return response.bad_request('The given content does not match the accompanying field type.')

                if not data:
                    old_content.delete()
                    continue

                entry_utils.patch_entry_content(request.user, entry, old_content, field, data, journal.assignment)

            file_handling.remove_temp_user_files(request.user)

        req_data = request.data
        if 'content' in req_data:
            del req_data['content']
        if content_list:
            req_data['last_edited'] = datetime.now()
        serializer = serialize.EntrySerializer(entry, data=req_data, partial=True, context={'user': request.user})
        if not serializer.is_valid():
            response.bad_request()

        try:
            serializer.save()
        except ValueError:
            return response.bad_request('Invalid grade or published state.')
        if published and journal.sourcedid is not None and journal.grade_url is not None:
            payload = lti_grade.replace_result(journal)
        else:
            payload = dict()

        return response.success({'entry': serializer.data, 'lti': payload})

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
        if not request.user.is_authenticated:
            return response.unauthorized()
        pk = kwargs.get('pk')

        entry = Entry.objects.get(pk=pk)
        journal = entry.node.journal

        if not (journal.user == request.user or request.user.is_superuser):
            return response.forbidden('You are not allowed to delete someone else\'s entry.')

        if entry.grade:
            return response.forbidden('You cannot delete graded entries.')

        if entry.node.type == Node.ENTRYDEADLINE and \
           permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal'):
            return response.forbidden('You cannot delete deadlines.')

        if journal.assignment.due_date and journal.assignment.due_date < datetime.now() and \
           permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal'):
            return response.forbidden('You cannot delete an entry whose deadline deadline has already passed.')

        if (journal.assignment.unlock_date and journal.assignment.unlock_date > datetime.now()) or \
           (journal.assignment.lock_date and journal.assignment.lock_date < datetime.now()) and \
           permissions.has_assignment_permission(request.user, journal.assignment, 'can_have_journal'):
            return response.forbidden('You cannot delete a locked entry.')

        entry.node.delete()
        entry.delete()
        return response.success(description='Sucesfully deleted entry.')
