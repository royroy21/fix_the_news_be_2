from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

from fix_the_news.communications import models


@receiver(pre_save, sender=models.Communication)
def inactivate_communications(sender, instance, **kwargs):
    if not instance.active:
        return

    communication_type = instance.type
    sender.objects.filter(type=communication_type).update(active=False)

    if communication_type == models.Communication.DAILY:
        get_user_model().objects.all()\
            .update(has_viewed_daily_communication=False)
