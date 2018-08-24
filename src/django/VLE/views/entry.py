"""
entry.py.

In this file are all the entry api requests.
"""
from rest_framework import viewsets

from VLE.models import Journal, Node, Content, Field, EntryTemplate, Entry
import VLE.views.responses as response
import VLE.factory as factory
import VLE.utils as utils
from django.utils.timezone import now
import VLE.lti_grade_passback as lti_grade
import VLE.edag as edag
import VLE.permissions as permissions
import VLE.serializers as serialize


class EntryView(viewsets.ViewSet):
    """Entry view.

    This class creates the following api paths:
    GET /entries/ -- gets all the entries
    POST /entries/ -- create a new entry
    GET /entries/<pk> -- gets a specific entry
    PATCH /entries/<pk> -- partially update an entry
    DEL /entries/<pk> -- delete an entry
    """

    def create(request):
        """Create a new entry.

        Arguments:
        request -- the request that was send with
        jID -- the journal id
        tID -- the template id to create the entry with
        nID -- optional: the node to bind the entry to (only for entrydeadlines)
        content -- the list of {tag, data} tuples to bind data to a template field.
        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            jID, tID, content_list = utils.required_params(request.data, "jID", "tID", "content")
            nID, = utils.optional_params(request.data, "nID")
        except KeyError:
            return response.keyerror("jID", "tID", "content")

        try:
            journal = Journal.objects.get(pk=jID, user=request.user)

            template = EntryTemplate.objects.get(pk=tID)

            if nID:
                node = Node.objects.get(pk=nID, journal=journal)
                if node.type == Node.PROGRESS:
                    return response.bad_request('Passed node is a Progress node.')

                if node.entry:
                    if node.entry.grade is None:
                        if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                            return response.bad_request('The deadline has already passed.')

                        Content.objects.filter(entry=node.entry).all().delete()
                        node.entry.template = template
                        node.save()
                    else:
                        return response.bad_request('Can not overwrite entry, since it is already graded.')
                else:
                    if node.type == Node.ENTRYDEADLINE and node.preset.deadline < now():
                        return response.bad_request('The deadline has already passed.')

                    node.entry = factory.make_entry(template)
                    node.save()
            else:
                entry = factory.make_entry(template)
                node = factory.make_node(journal, entry)

            if journal.sourcedid is not None and journal.grade_url is not None:
                lti_grade.needs_grading(journal, node.id)

            for content in content_list:
                data = content['data']
                tag = content['tag']
                field = Field.objects.get(pk=tag)

                factory.make_content(node.entry, data, field)

            result = edag.get_nodes_dict(journal, request.user)
            added = -1
            for i, result_node in enumerate(result):
                if result_node['nID'] == node.id:
                    added = i
                    break

            return response.created(payload={'added': added,
                                             'nodes': edag.get_nodes_dict(journal, request.user)})
        except (Journal.DoesNotExist, EntryTemplate.DoesNotExist, Node.DoesNotExist):
            return response.not_found('Journal, Template or Node does not exist.')

    def partial_update(self, request, *args, **kwargs):
        """Update an existing entry.

        Arguments:
        request -- request data
            data -- the new data for the course
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the entry does not exists
            forbidden -- User not allowed to edit this entry
            unauthorized -- when the user is unauthorized to edit the entry
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new entry data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        pk = kwargs.get('pk')

        try:
            entry = Entry.objects.get(pk=pk)
        except Entry.DoesNotExist:
            return response.not_found('Entry')

        grade, published, template = utils.optional_params(request.data, "grade", "published", "template")

        journal = entry.node.journal
        if grade and \
           not permissions.has_assignment_permission(request.user, journal.assignment, 'can_grade_journal'):
            return response.forbidden('You cannot grade or publish entries.')

        if published is not None and \
           not permissions.has_assignment_permission(request.user, journal.assignment,
                                                     'can_publish_journal_grades'):
            return response.forbidden('You cannot publish entries.')

        if template and \
           not permissions.has_assignment_permission(request.user, journal.assignment, 'can_edit_journal'):
            return response.forbidden('You cannot publish entries.')

        serializer = serialize.EntrySerializer(entry, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()

        if published and journal.sourcedid is not None and journal.grade_url is not None:
            payload = lti_grade.replace_result(journal)
        else:
            payload = dict()
        payload['new_published'] = entry.published

        return response.success(serializer.data, payload={'new_published': entry.published})
