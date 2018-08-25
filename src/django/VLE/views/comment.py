"""
comment.py.

In this file are all the comment api requests.
"""
from rest_framework import viewsets

from VLE.serializers import CommentSerializer
from VLE.models import Comment, Entry, User, Assignment
import VLE.views.responses as response
import VLE.permissions as permissions
import VLE.serializers as serialize
import VLE.utils as utils
import VLE.factory as factory


class CommentView(viewsets.ViewSet):
    """Comment view.

    This class creates the following api paths:
    GET /comment/ -- gets all the comment
    POST /comment/ -- create a new comment
    PATCH /comment/<pk> -- partially update an comment
    DEL /comment/<pk> -- delete an comment
    """

    def list(self, request):
        """Get the comments belonging to an entry.

        Arguments:
        request -- request data
            entry_id -- entry ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when its not their own journal, or the user is not allowed to grade that journal
        On succes:
            success -- with a list of the comments belonging to the entry

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        # Try to get the entry_id of the request.
        try:
            entry_id = request.query_params['entry_id']
        except KeyError:
            entry_id = None

        # Try to get the Entry associated with the given entry_id.
        try:
            if entry_id:
                entry = Entry.objects.get(pk=entry_id)
        except Entry.DoesNotExist:
            return response.not_found('Entry')

        if entry.node.journal.user != request.user and \
           not permissions.has_assignment_permission(
                request.user, entry.node.journal.assignment, 'can_view_assignment_participants'):
            return response.forbidden('You are not allowed to view journals of other participants.')

        if permissions.has_assignment_permission(request.user, entry.node.journal.assignment,
                                                 'can_grade_journal'):
            comments = Comment.objects.filter(entry=entry)
        else:
            comments = Comment.objects.filter(entry=entry, published=True)

        serializer = CommentSerializer(comments, many=True)
        return response.success({'comments': serializer.data})

    def create(self, request):
        """Create a new comment.

        Arguments:
        request -- request data
            entry_id -- entry ID
            text -- comment text
            published -- publishment state

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            key_error -- missing keys
            not_found -- could not find the entry, author or assignment

        On success:
            succes -- with the assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            entry_id, text, published = utils.required_params(
                request.data, "entry_id", "text", "published")
        except KeyError:
            return response.keyerror("entry_id", "text", "published")

        try:
            entry = Entry.objects.get(pk=entry_id)
            assignment = Assignment.objects.get(journal__node__entry=entry)
        except (User.DoesNotExist, Entry.DoesNotExist):
            return response.not_found('User, Entry or assignment does not exist.')

        published = published and permissions.has_assignment_permission(request.user, assignment,
                                                                           'can_grade_journal')

        comment = factory.make_entrycomment(entry, request.user, text, published)
        return response.created(payload={'comment': serialize.entrycomment_to_dict(comment)})

    def retrieve(self, request, pk=None):
        """Is not implemented yet."""
        return response.response(501)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing comment.

        Arguments:
        request -- request data
            text -- comment text
        pk -- comment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            keyerror -- when comment_id or text is not set
            not found -- when the comment does not exists
            forbidden -- when the user is not allowed to comment
            unauthorized -- when the user is unauthorized to edit the assignment
        On success:
            success -- with the updated comment

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        comment_id = kwargs.get('pk')

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return response.not_found('Comment does not exist.')

        if not permissions.has_assignment_permission(request.user, comment.entry.node.journal.assignment,
                                                     'can_comment_journal'):
            return response.forbidden('You cannot comment on entries.')

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if not serializer.is_valid():
            response.bad_request()
        serializer.save()
        return response.success({'comment': serializer.data})

    def destroy(self, request, *args, **kwargs):
        """Delete an existing comment from an entry.

        Arguments:
        request -- request data
        pk -- comment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the comment or author does not exist
            forbidden -- when the user cannot delete the assignment
        On success:
            success -- with a message that the comment was deleted

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        comment_id = kwargs.get('pk')

        try:
            comment = Comment.objects.get(pk=comment_id)
            author = User.objects.get(pk=comment.author.id)
        except (Comment.DoesNotExist, User.DoesNotExist):
            return response.not_found('Comment or Author does not exist.')

        if request.user != author and not request.user.is_superuser:
            return response.forbidden()

        Comment.objects.get(id=comment_id).delete()
        return response.success(description='Succesfully deleted comment.')
