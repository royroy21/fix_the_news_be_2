from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from fix_the_news.likes import models


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Like
        fields = (
            'id',
            'comment',
            'date_created',
            'news_item',
            'topic',
            'user',
        )
        read_only_fields = (
            'id',
            'date_created',
        )

    def validate(self, attrs):
        self.enforce_object_not_already_liked(attrs)
        self.enforce_only_one_object_type_is_being_liked(attrs)
        return super().validate(attrs)

    likable_objects = [
        "comment",
        "news_item",
        "topic",
    ]

    def enforce_object_not_already_liked(self, attrs):
        for object_name in self.likable_objects:
            obj = attrs.get(object_name)
            if not obj:
                continue
            query = obj.likes.filter(**{
                object_name: obj,
                "user": self.context["request"].user,
            })
            if query.exists():
                raise ValidationError({
                    "non_field_errors": ["You have liked this already"],
                })

    def enforce_only_one_object_type_is_being_liked(self, attrs):
        objects = [
            attrs[object_name]
            for object_name
            in self.likable_objects
            if attrs.get(object_name)
        ]
        if len(objects) > 1:
            raise ValidationError({
                "non_field_errors": ["You can only like one "
                                     "object type at a time"],
            })
