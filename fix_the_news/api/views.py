from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from fix_the_news.users import models


class CustomCreateModelMixin(GenericViewSet, mixins.CreateModelMixin):

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = self.get_user(request).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    def get_user(self, request):
        if request.user.is_authenticated:
            return request.user
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ipaddress = x_forwarded_for.split(',')[0]
        else:
            ipaddress = request.META.get('REMOTE_ADDR')
        return models.User.get_or_create_anonymous_user(ipaddress)


class CustomListModelMixin(GenericViewSet, mixins.ListModelMixin):

    allowed_filters = []

    def get_queryset(self):
        filters = {
            key: self.request.query_params.get(key)
            for key
            in self.allowed_filters
            if self.request.query_params.get(key)
        }
        return super().get_queryset().filter(**filters)


class CustomCreateRetrieveListViewSet(CustomCreateModelMixin,
                                      CustomListModelMixin,
                                      mixins.RetrieveModelMixin):
    pass


class CustomModelViewSet(CustomCreateModelMixin,
                         CustomListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    pass
