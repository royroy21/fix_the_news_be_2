from datetime import timedelta

from django_dynamic_fixture import G
from django.test import TestCase
from django.utils import timezone

from fix_the_news.news_items import models
from fix_the_news.likes import models as likes_models
from fix_the_news.news_items.services import scoring_service


class TestNewsItemScoringService(TestCase):

    service = scoring_service.NewsItemScoringService()

    def test_get_total_score_for_first_day(self):
        news_item = G(models.NewsItem)
        G(
            likes_models.Like,
            news_item=news_item,
            date_created=timezone.now() - timedelta(days=1),
        )
        score = self.service.get_score(news_item)

        self.assertEqual(score['this_week_score']['total_score'], 0)
        self.assertEqual(score['last_week_score']['total_score'], 0)
        self.assertEqual(score['third_week_score']['total_score'], 0)
        self.assertEqual(score['the_rest_score']['total_score'], 0)

        likes_score = score['last_few_days_score']['likes_score']
        multiplier = score['last_few_days_score']['multiplier']
        self.assertEqual(likes_score, self.service.LIKES_MULTIPLIER)
        self.assertEqual(multiplier, self.service.FIRST_FEW_DAYS_MULTIPLIER)
        expected_last_week_score = likes_score * multiplier
        self.assertEqual(
            expected_last_week_score,
            score['last_few_days_score']['total_score']
        )

    def test_get_total_score_for_second_week(self):
        news_item = G(models.NewsItem)
        G(
            likes_models.Like,
            news_item=news_item,
            date_created=timezone.now() - timedelta(days=10),
        )
        score = self.service.get_score(news_item)

        self.assertEqual(score['last_few_days_score']['total_score'], 0)
        self.assertEqual(score['this_week_score']['total_score'], 0)
        self.assertEqual(score['third_week_score']['total_score'], 0)
        self.assertEqual(score['the_rest_score']['total_score'], 0)

        likes_score = score['last_week_score']['likes_score']
        multiplier = score['last_week_score']['multiplier']
        self.assertEqual(likes_score, self.service.LIKES_MULTIPLIER)
        self.assertEqual(multiplier, self.service.LAST_WEEK_MULTIPLIER)
        expected_last_week_score = likes_score * multiplier
        self.assertEqual(
            expected_last_week_score,
            score['last_week_score']['total_score']
        )

    def test_get_total_score_for_rest(self):
        news_item = G(models.NewsItem)
        G(
            likes_models.Like,
            news_item=news_item,
            date_created=timezone.now() - timedelta(days=60),
        )
        score = self.service.get_score(news_item)

        self.assertEqual(score['last_few_days_score']['total_score'], 0)
        self.assertEqual(score['this_week_score']['total_score'], 0)
        self.assertEqual(score['last_week_score']['total_score'], 0)
        self.assertEqual(score['third_week_score']['total_score'], 0)

        likes_score = score['the_rest_score']['likes_score']
        multiplier = score['the_rest_score']['multiplier']
        self.assertEqual(likes_score, self.service.LIKES_MULTIPLIER)
        self.assertEqual(multiplier, 1)
        expected_last_week_score = likes_score * multiplier
        self.assertEqual(
            expected_last_week_score,
            score['the_rest_score']['total_score']
        )
