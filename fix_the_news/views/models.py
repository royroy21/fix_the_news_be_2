from django.db import models

from fix_the_news.core.models import DateCreatedUpdatedMixin


class View(DateCreatedUpdatedMixin):
    news_item = models.ForeignKey(
        'news_items.NewsItem',
        on_delete=models.CASCADE,
        related_name='views',
    )
    ip_address = models.CharField(max_length=254)

    def __str__(self):
        return f'{self.news_item.id} from ip address {self.ip_address}'
