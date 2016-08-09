#
# models.py

from django.db import models

class Verification(models.Model):
    """
    links a django user with a Trulioo verification id and the result of the match
    """

    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', null=True)
    transaction = models.CharField(max_length=255, null=False)
    transaction_record = models.CharField(max_length=255, null=False)
    record_status = models.CharField(max_length=255, null=False)
