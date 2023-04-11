from rest_framework import serializers

from fix_the_news.subscriptions import models


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subscription
        fields = (
            "id",
            "email",
        )
        read_only_fields = (
            "id",
        )
