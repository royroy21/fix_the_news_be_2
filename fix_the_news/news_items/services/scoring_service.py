from fix_the_news.core.services.scoring_service import BaseScoringService
from fix_the_news.likes import models as likes_models
from fix_the_news.views import models as views_models


class NewsItemScoringService(BaseScoringService):
    """
    Scoring is based upon how many likes and views a news item collects.

    Scoring is weighted so that likes and views are worth more the earlier
    they are created. For example likes and views in the first week would
    be scored using a much higher multiplier than the second week. This is
    so news items will score less over time unless they keep acquiring more
    likes and views.
    """
    FIRST_FEW_DAYS_MULTIPLIER = 10
    THIS_WEEK_MULTIPLIER = 5
    LAST_WEEK_MULTIPLIER = 3
    THIRD_WEEK_MULTIPLIER = 2

    LIKES_MULTIPLIER = 4
    VIEWS_MULTIPLIER = 1

    def get_score(self, news_item):
        dates = self.get_dates()

        last_few_days_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.FIRST_FEW_DAYS_MULTIPLIER,
            start_date=dates['last_few_days']['start'],
            end_date=dates['last_few_days']['end'],
        )
        this_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.THIS_WEEK_MULTIPLIER,
            start_date=dates['this_week']['start'],
            end_date=dates['this_week']['end'],
        )
        last_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.LAST_WEEK_MULTIPLIER,
            start_date=dates['last_week']['start'],
            end_date=dates['last_week']['end'],
        )
        third_week_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=self.THIRD_WEEK_MULTIPLIER,
            start_date=dates['third_week']['start'],
            end_date=dates['third_week']['end'],
        )
        the_rest_score = self.calculate_score_for_time_period(
            news_item=news_item,
            multiplier=1,
            end_date=dates['third_week']['start'],
        )

        total_score = (
            last_few_days_score['total_score']
            + this_week_score['total_score']
            + last_week_score['total_score']
            + third_week_score['total_score']
            + the_rest_score['total_score']
        )
        return {
            'last_few_days_score': last_few_days_score,
            'this_week_score': this_week_score,
            'last_week_score': last_week_score,
            'third_week_score': third_week_score,
            'the_rest_score': the_rest_score,
            'total_score': total_score,
        }

    def calculate_score_for_time_period(
            self, news_item, multiplier, start_date=None, end_date=None):
        likes_score = self.calculate_score_for_model(
            model=likes_models.Like,
            news_item=news_item,
            multiplier=self.LIKES_MULTIPLIER,
            start_date=start_date,
            end_date=end_date,
        )
        views_score = self.calculate_score_for_model(
            model=views_models.View,
            news_item=news_item,
            multiplier=self.VIEWS_MULTIPLIER,
            start_date=start_date,
            end_date=end_date,
        )
        return {
            'likes_score': likes_score,
            'views_score': views_score,
            'multiplier': multiplier,
            'total_score': (likes_score + views_score) * multiplier,
        }

    def calculate_score_for_model(
            self, model, news_item, multiplier,
            start_date=None, end_date=None):
        args = {
            'news_item': news_item,
        }
        if start_date:
            args['date_created__gte'] = start_date
        if end_date:
            args['date_created__lte'] = end_date

        query = model.objects.filter(**args)
        if query:
            return query.count() * multiplier
        else:
            return 0

    def get_highest_score(self, topic, category):
        """
        Gets highest score for news items of
        the same topic in the same category
        """
        top_scored_news_item = topic\
            .news_items.filter(category=category)\
            .order_by('-score')\
            .first()
        if not top_scored_news_item:
            return 0 + self.HIGHEST_SCORE_ADDITION
        else:
            return top_scored_news_item.score + self.HIGHEST_SCORE_ADDITION
