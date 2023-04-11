from datetime import timedelta

from django.utils import timezone


class BaseScoringService:

    LAST_FEW_DAYS = 2  # how many days count as first few days
    HIGHEST_SCORE_ADDITION = 10  # added to the result of get_highest_score

    def get_score(self, *args, **kwargs):
        raise NotImplementedError

    def get_highest_score(self, *args, **kwargs):
        raise NotImplementedError

    def get_dates(self):
        now = timezone.now()
        last_few_days = now - timedelta(days=self.LAST_FEW_DAYS)
        this_week = last_few_days - timedelta(days=7 - self.LAST_FEW_DAYS)
        last_week = this_week - timedelta(days=7)
        third_week = last_week - timedelta(days=7)
        return {
            'last_few_days': {'start': last_few_days, 'end': now},
            'this_week': {'start': this_week, 'end': last_few_days},
            'last_week': {'start': last_week, 'end': this_week},
            'third_week': {'start': third_week, 'end': last_week},
        }
