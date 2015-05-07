#
# keyprefix/models.py

from django.db import models

class KeyPrefix(models.Model):
    created     = models.DateTimeField(auto_now_add=True, null=True)
    prefix      = models.CharField(max_length=16, null=False)