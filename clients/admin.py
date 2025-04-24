from django.contrib import admin
from .models import Client

from django.utils.html import format_html

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'media_link', 'created_at')
    search_fields = ('name', 'email', 'phone')
    list_filter = ('created_at', 'updated_at')

    def media_link(self, obj):
        if obj.media:
            return format_html('<a href="{}" target="_blank">Open File</a>', obj.media.url)
        return "-"
    media_link.short_description = 'Media File'
