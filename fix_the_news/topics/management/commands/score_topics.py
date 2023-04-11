from django.core.management.base import BaseCommand

from fix_the_news.topics.tasks import score_all_topics


class Command(BaseCommand):
    help = "Scores all topics"

    def handle(self, *args, **options):
        score_all_topics()
