from django.test import TestCase
from django.urls import reverse
from django.utils.text import slugify
from django_dynamic_fixture import G
from rest_framework import status

from rest_framework.test import APIClient

from fix_the_news.topics import models


class TestTopicViewSet(TestCase):

    list_endpoint = reverse("topic-list")

    def setUp(self):
        self.authenticated_client = APIClient()
        self.unauthenticated_client = APIClient()
        self.topic_title = "Just in - Cats are amazing!"
        self.topic = G(
            models.Topic,
            title=self.topic_title,
            slug=slugify(self.topic_title),
        )

    def test_get_topic_by_slug(self):
        endpoint = reverse("topic-detail", kwargs={"slug": self.topic.slug})
        response = self.authenticated_client.get(endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.topic_title)

    def test_create_new_topic_with_unauthenticated_user(self):
        topic_title = "My cat is the best ever!"
        data = {
            "title": topic_title,
        }
        response = \
            self.authenticated_client.post(self.list_endpoint, data=data)
        self.assertEqual(response.status_code, 201)

        topic = models.Topic.objects\
            .filter(title=topic_title, active=False)\
            .first()
        self.assertTrue(topic)
        self.assertEqual(topic.user.name, "anonymous")
