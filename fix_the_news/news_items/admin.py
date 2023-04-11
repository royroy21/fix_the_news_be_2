from django.contrib import admin

from fix_the_news.news_items import models


class NewsItemAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "score",
        "date_created",
    )
    list_filter = (
        "topic__title",
    )
    ordering = (
        "date_created",
    )
    search_fields = (
        "title",
        "topic__title",
        "user__email",
        "user__first_name",
        "user__last_name",
        "url",
        "category__title",
    )


class NewsSourceFilter(admin.SimpleListFilter):
    title = "has formatted name"
    parameter_name = "has_formatted_name"

    def lookups(self, request, model_admin):
        return (
            ("yes", "Yes"),
            ("no",  "No"),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(formatted_name="")
        if self.value() == 'no':
            return queryset.filter(formatted_name="")


class NewsSourceAdmin(admin.ModelAdmin):
    list_filter = (
        NewsSourceFilter,
    )
    ordering = (
        "hostname",
    )
    search_fields = (
        "hostname",
        "formatted_name",
    )


admin.site.register(models.NewsItem, NewsItemAdmin)
admin.site.register(models.NewsSource, NewsSourceAdmin)
