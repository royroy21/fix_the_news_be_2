import random

from django.db import migrations


def assign_users(apps, schema_editor):
    names = [
        "Oliver Ben",
        "George01",
        "Noah",
        "Arthur",
        "Harry",
        "Leo",
        "Muhammad",
        "Mo",
        "Jack",
        "Charlie1984",
        "Oscar W",
        "Olly",
        "Amelia Peters",
        "Isla",
        "Sophia",
        "Freya",
        "The GOAT",
    ]
    User = apps.get_model('users', 'User')
    for name in names:
        User.objects.create(
            email=f"{'_'.join(name.split(' '))}@example.com",
            name=name,
        )
    Topic = apps.get_model('topics', 'Topic')
    for topic in Topic.objects.all():
        topic.user = User.objects.get(name=random.choice(names))
        topic.save()
    NewsItem = apps.get_model('news_items', 'NewsItem')
    for news_item in NewsItem.objects.all():
        news_item.user = User.objects.get(name=random.choice(names))
        news_item.save()
    Comment = apps.get_model('comments', 'Comment')
    for comment in Comment.objects.all():
        comment.user = User.objects.get(name=random.choice(names))
        comment.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_first_and_last_name_fields'),
    ]

    operations = [
        migrations.RunPython(assign_users, noop),
    ]
