from django.contrib.postgres.fields import JSONField
from django.db import models


class PusherWebhook(models.Model):
    """
    Pusher will optionally send us webhooks for various events. Things like 'user connected' or
    'channel empty'. We don't currently make use of the webhooks and they are disabled via Pusher's
    web admin console. Any incoming hooks arez are saved here... for some reason.
    """
    created = models.DateTimeField(auto_now_add=True)
    callback = JSONField()
