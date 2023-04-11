from django.db import models

from fix_the_news.core.models import DateCreatedUpdatedMixin


class Communication(DateCreatedUpdatedMixin):
    active = models.BooleanField(
        default=False,
        help_text='Setting a communication to active will set all other '
                  'communications of the same type to False. The frontend'
                  ' app will be update next time it calls the user API',
    )
    title = models.CharField(max_length=254, default='')
    text = models.TextField(default='')

    ABOUT = 'about'
    DAILY = 'daily'
    PRIVACY = 'privacy'
    REGISTRATION = 'registration'
    TERMS_AND_CONDITIONS = 'terms_and_conditions'
    WELCOME = 'welcome'
    TYPE_CHOICES = [
        (ABOUT, 'about'),
        (DAILY, 'daily'),
        (PRIVACY, 'privacy'),
        (REGISTRATION, 'registration'),
        (TERMS_AND_CONDITIONS, 'terms_and_conditions'),
        (WELCOME, 'welcome'),
    ]
    type = models.CharField(
        choices=TYPE_CHOICES,
        max_length=50,
    )

    def __str__(self):
        if len(self.text) > 100:
            return f'{self.text[:100]}...'
        else:
            return self.text

    def save(self, *args, **kwargs):
        if self.active:
            pass
        super().save(*args, **kwargs)
