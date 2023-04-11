from rest_framework import serializers

from fix_the_news.api.users import serializers as users_serializers
from fix_the_news.comments import models


class CommentSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    serialized_user = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'comment',
            'comments_count',
            'date_created',
            'news_item',
            'topic',
            'serialized_user',
            'text',
            'user',
        )
        read_only_fields = (
            'id',
            'comments_count',
            'date_created',
            'serialized_user',
        )

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_serialized_user(self, obj):
        return users_serializers\
            .UserReadOnlySerializer(
                obj.user,
                context={'request': self.context['request']})\
            .data
