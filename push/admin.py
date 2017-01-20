from django.contrib import admin

from push.models import PusherWebhook


@admin.register(PusherWebhook)
class PusherWebhookAdmin(admin.ModelAdmin):
    list_display = ['created', 'ts', 'callback']

    def ts(self, obj):
        return int(obj.created.strftime('%s'))
