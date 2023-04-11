from django.contrib import admin

from fix_the_news.comments import models


class CommentAdmin(admin.ModelAdmin):
    ordering = (
        'date_created',
    )
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
    )


admin.site.register(models.Comment, CommentAdmin)
