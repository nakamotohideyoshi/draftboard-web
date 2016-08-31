#
# admin.py

from django.contrib import admin
import swish.models

@admin.register(swish.models.History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['created', 'parsed_at', 'http_status', 'data']
    list_filter = ['created', 'http_status', 'data']
    search_fields = ['created', 'http_status', 'data']

    def parsed_at(self, obj):
        return int(obj.created.strftime('%s'))

@admin.register(swish.models.PlayerLookup)
class PlayerLookupAdmin(admin.ModelAdmin):
    list_display = ['created','updated','player','pid']
    list_filter = ['created','updated','pid']