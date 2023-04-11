from fix_the_news.api.users import serializers
from fix_the_news.api.views import CustomCreateModelMixin
from fix_the_news.users import models


class MessageViewSet(CustomCreateModelMixin):
    serializer_class = serializers.MessageSerializer
    queryset = models.Message.objects.all()
