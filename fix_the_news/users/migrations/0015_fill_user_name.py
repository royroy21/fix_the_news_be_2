from django.contrib.auth import get_user_model
from django.db import migrations


def fill_user_name(apps, schema_editor):
    User = get_user_model()
    for user in User.objects.all():
        try:
            user.name = f"{user.first_name} {user.last_name}"
            user.save()
        except:
            pass


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_user_name'),
    ]

    operations = [
        migrations.RunPython(fill_user_name, noop),
    ]
