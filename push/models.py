#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField

class PusherWebhook(models.Model):

    created = models.DateTimeField(auto_now_add=True)

    callback = JSONField()

