from copy import deepcopy

from django.db.models import Count
from rest_framework import serializers

from fix_the_news.api.users import serializers as users_serializers
from fix_the_news.topics import models


class CategoryReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'id',
            'title',
            'type',
        )
        read_only_fields = fields


class TopicSerializer(serializers.ModelSerializer):

    comments_count = serializers.SerializerMethodField()
    serialized_categories = serializers.SerializerMethodField()
    news_items_count = serializers.SerializerMethodField()
    total_news_items_count = serializers.SerializerMethodField()
    serialized_user = serializers.SerializerMethodField()
    is_shared = serializers.SerializerMethodField()
    number_of_likes = serializers.SerializerMethodField()
    last_updated = serializers.SerializerMethodField()

    class Meta:
        model = models.Topic
        fields = (
            'id',
            'comments_count',
            'date_created',
            'is_shared',
            'last_updated',
            'news_items_count',
            'number_of_likes',
            'serialized_user',
            'score',
            'serialized_categories',
            'slug',
            'title',
            'total_news_items_count',
            'user',
        )
        read_only_fields = (
            'id',
            'comments_count',
            'date_created',
            'is_shared',
            'last_updated',
            'news_items_count',
            'number_of_likes',
            'serialized_user',
            'score',
            'serialized_categories',
            'slug',
            'total_news_items_count',
        )

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_is_shared(self, obj):
        """
        Indicates if the user is getting the topic via a shared link.
        """
        return False

    def get_last_updated(self, obj):
        last_added_news_item = obj.news_items.order_by('date_created').last()
        if last_added_news_item:
            return last_added_news_item.date_created
        return obj.date_created

    def get_news_items_count(self, obj):
        return {
            key: obj.news_items.filter(active=True, category__type=key).count()
            for key
            in models.Category.ALL_TYPE_CHOICES
        }

    def get_number_of_likes(self, obj):
        return obj.news_items.aggregate(Count("likes"))["likes__count"]

    def get_total_news_items_count(self, obj):
        return obj.news_items.filter(active=True).count()

    def get_serialized_categories(self, obj):
        """ Returns serialized categories sorted by category type choices """
        data_with_key = {
            category["type"]: category
            for category
            in CategoryReadOnlySerializer(obj.categories.all(), many=True).data
        }
        return [
            data_with_key[category_type]
            for category_type, _
            in models.Category.TYPE_CHOICES
        ]

    def get_serialized_user(self, obj):
        return users_serializers\
            .UserReadOnlySerializer(
                obj.user,
                context={'request': self.context['request']})\
            .data

    def create(self, validated_data):
        """
        Topics created through this serializer have active set as False.
        This is because topics created by users have to be vetted first
        before published.
        """
        validated_data_copy = deepcopy(validated_data)
        validated_data_copy['active'] = False
        return super().create(validated_data_copy)
