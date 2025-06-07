from unfold.admin import ModelAdmin
from .models import LinkMapped
from django.contrib import admin


@admin.register(LinkMapped)
class LinkMappedAdmin(ModelAdmin):
    list_display = ('original_url', 'url_hash')
    search_fields = ('original_url', 'url_hash')
    readonly_fields = ('url_hash',)
    fieldsets = (
        (None, {
            'fields': ('original_url', 'url_hash')
        }),
    )
    ordering = ('-id',)
