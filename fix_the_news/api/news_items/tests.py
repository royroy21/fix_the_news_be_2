from unittest.mock import patch

from django_dynamic_fixture import G
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from fix_the_news.news_items import models
from fix_the_news.topics import models as topics_models
from fix_the_news.users import models as users_models
from fix_the_news.views import models as views_models


class TestNewsItemViewSet(TestCase):

    list_endpoint = reverse("newsitem-list")

    def setUp(self):
        self.unauthenticated_client = APIClient()
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=G(users_models.User))

        self.topic = G(topics_models.Topic)
        self.for_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_FOR,
            topic=self.topic,
        )
        self.neutral_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_NEUTRAL,
            topic=self.topic,
        )
        self.against_category = G(
            topics_models.Category,
            type=topics_models.Category.TYPE_AGAINST,
            topic=self.topic,
        )
        self.for_news_item = G(
            models.NewsItem,
            category=self.for_category,
            title="This news item is for",
        )
        self.neutral_news_item = G(
            models.NewsItem,
            category=self.neutral_category,
            title="This news item is neutral",
        )
        self.against_news_item = G(
            models.NewsItem,
            category=self.against_category,
            title="This news item is against",
        )

    def test_delete(self):
        # Users should not be able to delete news items
        detail_endpoint = \
            reverse("newsitem-detail", kwargs={"pk": self.for_news_item})
        response = self.unauthenticated_client.delete(detail_endpoint)
        self.assertEqual(response.status_code, 405)
        news_item_exists = \
            models.NewsItem.objects.filter(id=self.for_news_item.id).exists()
        self.assertTrue(news_item_exists)

    def get_create_new_news_item_data(self):
        return {
            "title": "A new news item",
            "topic": self.topic.id,
            "url": "www.news.com",
            "category": self.for_category.id,
        }

    @patch('requests.get')
    def test_create_with_authenticated_user(self, mock_request):
        mock_request.ok = True

        data = self.get_create_new_news_item_data()
        response = \
            self.authenticated_client.post(self.list_endpoint, data=data)
        self.assertEqual(response.status_code, 201)
        news_item_exists = \
            models.NewsItem.objects.filter(title=data["title"]).exists()
        self.assertTrue(news_item_exists)

    @patch('requests.get')
    def test_create_with_unauthenticated_user(self, mock_request):
        mock_request.ok = True

        data = self.get_create_new_news_item_data()
        response = \
            self.unauthenticated_client.post(self.list_endpoint, data=data)
        self.assertEqual(response.status_code, 201)
        news_item_exists = \
            models.NewsItem.objects.filter(title=data["title"]).exists()
        self.assertTrue(news_item_exists)

    def test_add_view(self):
        news_item = G(models.NewsItem, views=0)
        endpoint = reverse('newsitem-add-view', kwargs={'pk': news_item.id})

        # first view
        response = self.unauthenticated_client.post(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        query = views_models.View.objects.filter(news_item=news_item)
        self.assertEqual(query.count(), 1)

        # second view
        response = self.unauthenticated_client.post(endpoint)
        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
