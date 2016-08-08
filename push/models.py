#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField

class PusherWebhook(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    callback = JSONField()

class Sent(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    channel = models.CharField(max_length=64, null=False)
    event = models.CharField(max_length=64, null=False)

    api_response = JSONField()

    data = JSONField()


