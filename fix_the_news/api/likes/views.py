from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from fix_the_news.api.likes import serializers
from fix_the_news.api.views import CustomCreateModelMixin
from fix_the_news.likes import models


class LikeViewSet(CustomCreateModelMixin, mixins.DestroyModelMixin):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.LikeSerializer
    queryset = models.Like.objects.order_by("-date_created")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.user != request.user:
            return Response(
                {'non_field_errors': ['you can only delete your own likes']},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)
