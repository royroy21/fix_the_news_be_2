from django.core.management.base import BaseCommand

from fix_the_news.news_items.tasks import score_all_news_items


class Command(BaseCommand):
    help = "Scores all news items"

    def handle(self, *args, **options):
        score_all_news_items()
