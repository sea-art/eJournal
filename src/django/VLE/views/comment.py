"""
comment.py.

In this file are all the comment api requests.
"""
from rest_framework import viewsets

import VLE.factory as factory
import VLE.utils.generic_utils as utils
import VLE.utils.responses as response
from VLE.models import Comment, Entry
from VLE.serializers import CommentSerializer
from VLE.utils import file_handling


class CommentView(viewsets.ViewSet):
    """Comment view.

    This class creates the following api paths:
    GET /comment/ -- gets all the comments of the specific entry
    POST /comment/ -- create a new comment
    GET /comment/<pk> -- gets a specific comment
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
            not found -- when the course does not exist
            forbidden -- when its not their own journal, or the user is not allowed to grade that journal
        On success:
            success -- with a list of the comments belonging to the entry

        """
        entry_id, = utils.required_params(request.query_params, "entry_id")

        entry = Entry.objects.get(pk=entry_id)
        journal = entry.node.journal
        assignment = journal.assignment

        request.user.check_can_view(journal)

        if request.user.has_permission('can_grade', assignment):
            comments = Comment.objects.filter(entry=entry)
        else:
            comments = Comment.objects.filter(entry=entry, published=True)

        serializer = CommentSerializer(comments, context={'user': request.user}, many=True)
        return response.success({'comments': serializer.data})

    def create(self, request):
        """Create a new comment.

        Arguments:
        request -- request data
            entry_id -- entry ID
            text -- comment text
            published -- published state

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            key_error -- missing keys
            not_found -- could not find the entry, author or assignment

        On success:
            success -- with the assignment data

        """
        entry_id, text, = utils.required_params(request.data, 'entry_id', 'text')
        published, = utils.optional_typed_params(request.data, (bool, 'published'))

        entry = Entry.objects.get(pk=entry_id)
        journal = entry.node.journal
        assignment = journal.assignment

        request.user.check_permission('can_comment', assignment)
        request.user.check_can_view(journal)

        # By default a comment will be published, only users who can grade can delay publishing.
        published = published or not request.user.has_permission('can_grade', assignment)
        comment = factory.make_comment(entry, request.user, text, published)
        file_handling.establish_rich_text(request.user, text, comment=comment)
        file_handling.remove_unused_user_files(request.user)
        return response.created({'comment': CommentSerializer(comment, context={'user': request.user}).data})

    def retrieve(self, request, pk=None):
        """Retrieve a comment.

        Arguments:
        request -- request data
        pk -- assignment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not_found -- could not find the course with the given id
            forbidden -- not allowed to retrieve assignments in this course

        On success:
            success -- with the comment data

        """
        comment = Comment.objects.get(pk=pk)
        request.user.check_can_view(comment)

        serializer = CommentSerializer(comment, context={'user': request.user})
        return response.success({'comment': serializer.data})

    def partial_update(self, request, *args, **kwargs):
        """Update an existing comment.

        Arguments:
        request -- request data
            text -- comment text
        pk -- comment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the comment does not exist
            forbidden -- when the user is not allowed to comment
            unauthorized -- when the user is unauthorized to edit the assignment
        On success:
            success -- with the updated comment

        """
        comment_id, = utils.required_typed_params(kwargs, (int, 'pk'))

        comment = Comment.objects.get(pk=comment_id)
        journal = comment.entry.node.journal
        assignment = journal.assignment

        request.user.check_permission('can_comment', assignment)
        request.user.check_can_view(journal)

        if not comment.can_edit(request.user):
            return response.forbidden('You are not allowed to edit this comment.')

        comment.last_edited_by = request.user
        comment.save()
        text, = utils.required_params(request.data, 'text')
        serializer = CommentSerializer(
            comment, data={'text': text}, context={'user': request.user}, partial=True)
        if not serializer.is_valid():
            return response.bad_request()
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
        comment_id, = utils.required_typed_params(kwargs, (int, 'pk'))
        comment = Comment.objects.get(pk=comment_id)

        request.user.check_can_view(comment)

        if not comment.can_edit(request.user):
            return response.forbidden(description='You are not allowed to delete this comment.')

        comment.delete()
        return response.success(description='Successfully deleted comment.')
