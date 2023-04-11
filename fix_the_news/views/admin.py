from django.contrib import admin

from fix_the_news.views import models


class ViewAdmin(admin.ModelAdmin):
    ordering = (
        "date_created",
    )
    search_fields = (
        "news_item__id",
        "news_item__title",
        "ip_address",
    )


admin.site.register(models.View, ViewAdmin)
