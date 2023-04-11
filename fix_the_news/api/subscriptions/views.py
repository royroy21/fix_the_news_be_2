from fix_the_news.api.subscriptions import serializers
from fix_the_news.api.views import CustomCreateModelMixin
from fix_the_news.subscriptions import models


class SubscriptionViewSet(CustomCreateModelMixin):
    serializer_class = serializers.SubscriptionSerializer
    queryset = models.Subscription.objects.all()
