from rest_framework import viewsets

from fix_the_news.api.communications import serializers
from fix_the_news.communications import models


class CommunicationViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field = 'type'
    serializer_class = serializers.CommunicationReadOnlySerializer
    queryset = models.Communication.objects.filter(active=True)
