"""
comment.py.

In this file are all the comment api requests.
"""
from rest_framework import viewsets

from VLE.serializers import CommentSerializer
from VLE.models import Comment


class CommentView(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.all()
