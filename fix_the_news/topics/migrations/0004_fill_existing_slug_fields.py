from django.db import migrations
from django.utils.text import slugify


def fill_existing_slug_fields(apps, schema_editor):
    Topic = apps.get_model('topics', 'Topic')
    for topic in Topic.objects.all():
        topic.slug = slugify(topic.title)
        topic.save()


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_topic_slug'),
    ]

    operations = [
        migrations.RunPython(fill_existing_slug_fields, noop),
    ]
