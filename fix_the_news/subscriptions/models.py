from django.db import models

from fix_the_news.core.models import DateCreatedUpdatedMixin
from fix_the_news.users.validators import EmailValidator


class Subscription(DateCreatedUpdatedMixin):
    email_validator = EmailValidator()
    email = models.CharField(
        max_length=254,
        validators=[email_validator],
    )

    def __str__(self):
        return f"#{self.id} {self.email}"
