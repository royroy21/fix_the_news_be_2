from djoser.serializers import TokenCreateSerializer as \
    DjoserTokenCreateSerializer
from rest_framework.validators import ValidationError


class TokenCreateSerializer(DjoserTokenCreateSerializer):

    def validate(self, attrs):
        email = attrs.get("email")

        if isinstance(email, str):
            email = email.lower()

        return super().validate({
            **attrs,
            "email": email,
        })

    def create(self, validated_data):
        raise ValidationError("Create method disabled.")

    def update(self, instance, validated_data):
        raise ValidationError("Update method disabled.")
