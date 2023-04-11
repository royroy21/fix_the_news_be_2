import csv
from datetime import datetime

import pytz
from django.core.management.base import BaseCommand

from fix_the_news.news_items import models as news_items_models
from fix_the_news.topics import models as topics_models
from fix_the_news.users import models as users_models


class Command(BaseCommand):
    DATA_FILE = "fix_the_news/topics/data/development_test_data.csv"
    help = f"Creates test data for development environment from {DATA_FILE}"

    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "cats"

    def handle(self, *args, **options):
        admin_query = users_models.User.objects.filter(email=self.ADMIN_EMAIL)
        if admin_query.exists():
            admin = admin_query.first()
        else:
            admin = users_models.User.objects.create_user(
                email=self.ADMIN_EMAIL,
                password=self.ADMIN_PASSWORD,
            )

        topics_ids = set()

        with open(self.DATA_FILE) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if len(row.keys()) != len(reader.fieldnames):
                    self.stdout.write(self.style.ERROR(
                        f"problem encountered: skipping row {row}"
                    ))

                user_query = users_models.User.objects.filter(
                    email=row["email"],
                )
                if user_query.exists():
                    user = user_query.first()
                else:
                    user = users_models.User.objects.create_user(
                        email=row["email"],
                        password="pa$$word",
                    )
                topic, _ = topics_models.Topic.objects.get_or_create(
                    user=admin,
                    title=row["topic_title"],
                )
                category = topics_models.Category.objects.get(
                    topic=topic,
                    type=row["topic_category"],
                )
                news_url = row["news_item_url"]
                news_source, _ = news_items_models.NewsSource.objects\
                    .get_or_create(hostname=news_url)
                news_item_title = row["news_item_title"]
                news_item, created = news_items_models.NewsItem.objects.get_or_create(
                    title=news_item_title,
                    topic=topic,
                    user=user,
                    url=news_url,
                    category=category,
                    news_source=news_source,
                )
                if created:
                    date_created = \
                        datetime.strptime(row["create_date"], "%Y-%m-%d")
                    timezone_aware_date = pytz.utc.localize(date_created)
                    news_item.date_created = timezone_aware_date
                    news_item.date_updated = timezone_aware_date
                    news_item.save()

                self.stdout.write(self.style.SUCCESS(
                    f"Created news item: {news_item_title}"
                ))
                topics_ids.add(topic.id)
