from django.contrib import admin

from fix_the_news.communications import models


class CommunicationAdmin(admin.ModelAdmin):
    list_display = (
        '__str__',
        'type',
        'active',
        'date_created',
    )
    list_filter = (
        'active',
        'type',
    )
    ordering = (
        '-active',
        'date_created',
    )


admin.site.register(models.Communication, CommunicationAdmin)
