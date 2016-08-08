#
# admin.py

from django.contrib import admin
from push.models import (
    PusherWebhook,
    Sent,
)

@admin.register(PusherWebhook)
class PusherWebhookAdmin(admin.ModelAdmin):

    list_display = ['created', 'ts', 'callback']

    def ts(self, obj):
        return int(obj.created.strftime('%s'))

@admin.register(Sent)
class SentAdmin(admin.ModelAdmin):

    list_display = ['created', 'ts', 'channel', 'event', 'api_response', 'data']
    list_filter = ['channel','event']
    search_fields = ['channel','event','api_response','data']

    def ts(self, obj):
        return int(obj.created.strftime('%s'))