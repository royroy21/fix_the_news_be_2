from django.core.management.base import BaseCommand

from fix_the_news.news_items.tasks import add_image_to_news_items


class Command(BaseCommand):
    help = "Adds images to news items"

    def handle(self, *args, **options):
        add_image_to_news_items()
