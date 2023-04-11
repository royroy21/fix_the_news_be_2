# Generated by Django 3.0.4 on 2020-08-12 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0006_added_score_and_priority_for_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='priority',
            field=models.BooleanField(default=False, help_text='If True moves this topic above other topics regardless of score'),
        ),
    ]
