from django.test import TestCase
from django.urls import reverse
from django_dynamic_fixture import G
from rest_framework.test import APIClient

from fix_the_news.comments import models
from fix_the_news.news_items import models as news_items_models
from fix_the_news.users import models as users_models


class TestCommentViewSet(TestCase):

    endpoint = reverse('comment-list')

    def setUp(self):
        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=G(users_models.User))

    def test_link_to_missing_comment(self):
        another_comment_text = 'another comment'
        data = {
            'comment': 999,
            'text': another_comment_text,
        }
        response = self.authenticated_client.post(
            self.endpoint,
            data=data,
        )
        self.assertEqual(response.status_code, 400)

    def test_link_to_comment(self):
        existing_comment = G(models.Comment, text='a comment')

        another_comment_text = 'another comment'
        data = {
            'comment': existing_comment.id,
            'text': another_comment_text,
        }
        response = self.authenticated_client.post(
            self.endpoint,
            data=data,
        )
        self.assertEqual(response.status_code, 201)

        existing_comment.refresh_from_db()
        self.assertEqual(
            existing_comment.comments.first().text,
            another_comment_text,
        )
        self.assertEqual(models.Comment.objects.all().count(), 2)

    def test_link_to_news_item(self):
        news_item = G(news_items_models.NewsItem)

        comment_text = 'a comment'
        data = {
            'news_item': news_item.id,
            'text': comment_text,
        }
        response = self.authenticated_client.post(
            self.endpoint,
            data=data,
        )
        self.assertEqual(response.status_code, 201)

        news_item.refresh_from_db()
        self.assertEqual(
            news_item.comments.first().text,
            comment_text,
        )
