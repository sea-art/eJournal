"""
comment.py.

In this file are all the comment api requests.
"""
from rest_framework import viewsets

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
    GET /comment/upcomming/ -- get the upcomming comment of the logged in user
    """

    def list(self, request):
        """Get the comments from an entry.

        Arguments:
        request -- request data
            cID -- course ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the course does not exists
            forbidden -- when the user is not part of the course
        On succes:
            success -- with the assignment data

        """
        # Check if the user is correctly authenticated.
        if not request.user.is_authenticated:
            return response.unauthorized()

        # Try to get the eID of the request.
        try:
            eID = request.query_params['eID']
        except KeyError:
            eID = None
        try:
            # Try to get the Entry associated with the given eID.
            if eID:
                entry = Entry.objects.get(pk=eID)
        except Entry.DoesNotExist:
            return response.not_found('Entry')

        if not (entry.node.journal.user == request.user or permissions.has_assignment_permission(request.user,
                entry.node.journal.assignment, 'can_view_assignment_participants')):
            return response.forbidden('You are not allowed to view journals of other participants.')

        if permissions.has_assignment_permission(request.user, entry.node.journal.assignment,
                                                 'can_grade_journal'):
            entrycomments = Comment.objects.filter(entry=entry)
        else:
            entrycomments = Comment.objects.filter(entry=entry, published=True)

        return response.success(payload={
            'entrycomments': [serialize.entrycomment_to_dict(comment) for comment in entrycomments]
        })

    def create(self, request):
        """Create a new comment.

        Arguments:
        request -- request data
            eID -- entry ID
            uID -- author ID
            text -- comment text
            published -- publishment state

        Returns:
            On failure:
                unauthorized -- when the user is not logged in
                not_found -- could not find the entry or author
                key_error -- missing keys
                forbidden -- the user is not allowed to write comments

            On success:
                succes -- with the assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            eID, uID, text, published = utils.required_params(request.data, "eID", "uID", "text", "published")
        except KeyError:
            return response.keyerror("eID", "uID", "text", "published")

        try:
            author = User.objects.get(pk=uID)
            entry = Entry.objects.get(pk=eID)
            assignment = Assignment.objects.get(journal__node__entry=entry)
        except (User.DoesNotExist, Entry.DoesNotExist):
            return response.not_found('User or Entry')

        if author is not request.user:
            return response.forbidden('You are not allowed to write comments for others.')

        published = published or not permissions.has_assignment_permission(request.user, assignment,
                                                                           'can_grade_journal')

        comment = factory.make_entrycomment(entry, author, text, published)
        return response.created(payload={'comment': serialize.entrycomment_to_dict(comment)})

    def retrieve(self, request, pk=None):
        """Is not implemented yet."""
        return response.response(501)

    def partial_update(self, request, *args, **kwargs):
        """Update an existing comment.

        Arguments:
        request -- request data
            commentID -- comment ID
            text -- comment text

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the comment does not exists
            forbidden -- User not allowed to comment
            unauthorized -- when the user is unauthorized to edit the assignment
            bad_request -- when there is invalid data in the request
        On success:
            success -- with the new assignment data

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        try:
            commentID, text = utils.required_params(request.data, "commentID", "text")
        except KeyError:
            return response.keyerror("commentID")

        try:
            comment = Comment.objects.get(pk=commentID)
        except Comment.DoesNotExist:
            return response.not_found('Comment does not exist.')

        if not permissions.has_assignment_permission(request.user, comment.entry.node.journal.assignment,
                                                     'can_comment_journal'):
            return response.forbidden('You cannot comment on entries.')

        comment.text = text
        comment.save()
        return response.success()

    def destroy(self, request, *args, **kwargs):
        """Delete an existing comment from an entry.

        Arguments:
        request -- request data
        pk -- comment ID

        Returns:
        On failure:
            unauthorized -- when the user is not logged in
            not found -- when the assignment or course does not exists
            unauthorized -- when the user is not logged in
            forbidden -- when the user cannot delete the assignment
        On success:
            success -- with a message that the course was deleted

        """
        if not request.user.is_authenticated:
            return response.unauthorized()

        comment_id = kwargs.get('pk')

        try:
            comment = Comment.objects.get(pk=comment_id)
            author = User.objects.get(pk=comment.author.id)
        except (Comment.DoesNotExist, User.DoesNotExist):
            return response.not_found('Comment or Author does not exist.')

        if request.user is not author:
            return response.forbidden()

        Comment.objects.get(id=comment_id).delete()
        return response.success(message='Succesfully deleted comment.')
