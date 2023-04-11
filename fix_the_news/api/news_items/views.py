from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from fix_the_news.api.news_items import serializers
from fix_the_news.api.pagination import CustomPageNumberPagination
from fix_the_news.api.views import CustomCreateRetrieveListViewSet
from fix_the_news.news_items import models
from fix_the_news.views import models as views_models


class NewsItemViewSet(CustomCreateRetrieveListViewSet):
    allowed_filters = [
        'category',
        'topic',
    ]
    pagination_class = CustomPageNumberPagination
    queryset = models.NewsItem.objects\
        .filter(active=True)\
        .order_by("-score", "-date_created")
    serializer_class = serializers.NewsItemSerializer

    @action(methods=['post'], detail=True, url_path='add-view')
    def add_view(self, request, *args, **kwargs):
        news_item = self.get_object()
        if not news_item:
            return Response(status=status.HTTP_404_NOT_FOUND)

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')

        query = views_models.View.objects.filter(
            news_item=news_item,
            ip_address=ip_address,
        )
        # Only record views from unique ip addresses
        if query:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        views_models.View.objects.create(
            news_item=news_item,
            ip_address=ip_address,
        )
        return Response(status=status.HTTP_200_OK)
