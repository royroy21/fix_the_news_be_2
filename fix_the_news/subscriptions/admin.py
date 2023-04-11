from django.contrib import admin

from fix_the_news.subscriptions import models


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "email",
    )
    ordering = (
        "date_created",
    )
    search_fields = (
        "email",
    )


admin.site.register(models.Subscription, SubscriptionAdmin)
