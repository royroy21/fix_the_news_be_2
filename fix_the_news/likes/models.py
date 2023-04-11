from django.db import models
from fix_the_news.core.models import DateCreatedUpdatedMixin


class Like(DateCreatedUpdatedMixin):
    comment = models.ForeignKey(
        'comments.Comment',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    news_item = models.ForeignKey(
        'news_items.NewsItem',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    topic = models.ForeignKey(
        'topics.Topic',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='likes',
    )
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.email}'
