# Generated by Django 4.1.7 on 2023-03-31 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
