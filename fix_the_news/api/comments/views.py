from rest_framework import status
from rest_framework.response import Response

from fix_the_news.api.comments import serializers
from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.views import CustomCreateRetrieveListViewSet
from fix_the_news.comments import models


class CommentViewSet(CustomCreateRetrieveListViewSet):
    allowed_filters = [
        'comment',
        'news_item',
        'topic',
    ]
    pagination_class = CustomPageNumberPagination
    queryset = models.Comment.objects\
        .filter(active=True)\
        .order_by("-date_created")
    serializer_class = serializers.CommentSerializer
