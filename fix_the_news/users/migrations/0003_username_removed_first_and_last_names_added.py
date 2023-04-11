# Generated by Django 3.0.4 on 2020-03-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_fix_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default='', max_length=254, verbose_name='first_name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default='', max_length=254, verbose_name='last_name'),
            preserve_default=False,
        ),
    ]
