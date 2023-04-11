from django.db import models
from fix_the_news.core.models import DateCreatedUpdatedMixin


class Comment(DateCreatedUpdatedMixin):
    active = models.BooleanField(default=True)
    comment = models.ForeignKey(
        'comments.Comment',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    news_item = models.ForeignKey(
        'news_items.NewsItem',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    topic = models.ForeignKey(
        'topics.Topic',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.user.email}'
