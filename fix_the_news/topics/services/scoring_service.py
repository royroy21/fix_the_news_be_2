from django.db.models import Sum

from fix_the_news.core.services.scoring_service import BaseScoringService
from fix_the_news.comments import models as comments_models
from fix_the_news.news_items import models as news_items_models
from fix_the_news.topics import models


class TopicScoringService(BaseScoringService):

    FIRST_FEW_DAYS_MULTIPLIER = 10
    THIS_WEEK_MULTIPLIER = 5
    LAST_WEEK_MULTIPLIER = 3
    THIRD_WEEK_MULTIPLIER = 2

    def get_score(self, topic):
        news_items_score = self.get_score_for_news_items(topic)
        comments_score = self.get_score_for_comments(topic)
        return news_items_score + comments_score

    def get_score_for_news_items(self, topic):
        score = news_items_models\
            .NewsItem.objects\
            .filter(topic=topic)\
            .aggregate(Sum('score'))['score__sum']
        if score is None:
            return 0
        else:
            return score

    def get_score_for_comments(self, topic):
        dates = self.get_dates()

        first_days_score = self.calculate_score_for_time_period(
            topic,
            multiplier=self.FIRST_FEW_DAYS_MULTIPLIER,
            start_date=dates['last_few_days']['start'],
            end_date=dates['last_few_days']['end'],
        )
        this_week_score = self.calculate_score_for_time_period(
            topic,
            multiplier=self.THIS_WEEK_MULTIPLIER,
            start_date=dates['this_week']['start'],
            end_date=dates['this_week']['end'],
        )
        last_week_score = self.calculate_score_for_time_period(
            topic,
            multiplier=self.LAST_WEEK_MULTIPLIER,
            start_date=dates['last_week']['start'],
            end_date=dates['last_week']['end'],
        )
        third_week_score = self.calculate_score_for_time_period(
            topic,
            multiplier=self.THIRD_WEEK_MULTIPLIER,
            start_date=dates['third_week']['start'],
            end_date=dates['third_week']['end'],
        )
        the_rest_score = self.calculate_score_for_time_period(
            topic,
            multiplier=1,
            start_date=None,
            end_date=dates['third_week']['end'],
        )

        score = (
            first_days_score
            + this_week_score
            + last_week_score
            + third_week_score
            + the_rest_score
        )
        return score

    def calculate_score_for_time_period(
            self, topic, multiplier, start_date=None, end_date=None):
        args = {
            'topic': topic,
        }
        if start_date:
            args['date_created__gte'] = start_date
        if end_date:
            args['date_created__lte'] = end_date
        comments = comments_models.Comment.objects.filter(**args).count()

        if comments:
            return comments * multiplier
        else:
            return 0

    def get_highest_score(self):
        """ Returns highest topic score """
        highest_scored_topic = models.Topic.objects.order_by('-score').first()
        if not highest_scored_topic:
            return 0 + self.HIGHEST_SCORE_ADDITION
        else:
            return highest_scored_topic.score + self.HIGHEST_SCORE_ADDITION
