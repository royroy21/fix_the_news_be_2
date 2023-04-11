from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.transaction import on_commit
from djoser.serializers import UserSerializer as DjoserUserSerializer
from djoser.serializers import UserCreateSerializer as \
    DjoserUserCreateSerializer
from rest_framework import serializers
from rest_framework.serializers import CharField

from fix_the_news.users import models
from fix_the_news.users.tasks import create_avatar_thumbnail

User = get_user_model()


class CurrentUserSerializer(DjoserUserSerializer):
    avatar = serializers.ImageField(
        allow_empty_file=True,
        allow_null=True,
        required=False,
    )

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.LOGIN_FIELD,
            "avatar",
            "avatar_thumbnail_small",
            "id",
            "name",
            "has_viewed_registration_communication",
            "has_viewed_daily_communication",
            "subscribe_to_emails",
        )
        read_only_fields = (
            "avatar_thumbnail_small",
            "id",
        )

    def save(self, **kwargs):
        if "avatar" in self.validated_data \
                and self.validated_data["avatar"] is None:
            self.validated_data["avatar_thumbnail_small"] = None
        user = super().save(**kwargs)
        if "avatar" in self.validated_data:
            on_commit(lambda: create_avatar_thumbnail(user.id))
        return user


class CreatePasswordRetypeSerializer(DjoserUserCreateSerializer):

    re_password = CharField(
        style={'input_type': 'password'},
        write_only=True,
    )

    default_error_messages = {
        'password_mismatch': 'Password fields do not match.',
    }

    class Meta:
        model = User
        fields = (
            settings.LOGIN_FIELD,
            "avatar",
            "password",
            "re_password",
            "name",
            "subscribe_to_emails",
        )

    def validate(self, attrs):
        re_password = attrs.pop('re_password')
        attrs = super().validate(attrs)
        if attrs['password'] != re_password:
            self.fail('password_mismatch')
        return attrs

    def save(self, **kwargs):
        if "avatar" in self.validated_data \
                and self.validated_data["avatar"] is None:
            self.validated_data["avatar_thumbnail_small"] = None
        user = super().save(**kwargs)
        if "avatar" in self.validated_data:
            on_commit(lambda: create_avatar_thumbnail(user.id))
        return user


class UserReadOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            "avatar",
            "avatar_thumbnail_small",
            "id",
            "name",
        )
        read_only_fields = fields


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Message
        fields = (
            'email',
            'text',
            'title',
            'type',
            'user',
        )
