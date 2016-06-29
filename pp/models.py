#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField

class AbstractPaymentData(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    payment_data = JSONField()

    class Meta:
        abstract = True

class SavedCardPaymentData(AbstractPaymentData):
    """
    for any response from paypal trying to make a payment
    """
    class Meta:
        abstract = False

class CreditCardPaymentData(AbstractPaymentData):
    """
    for any response from paypal trying to make a payment
    """
    class Meta:
        abstract = False

class PayPalAccountPaymentData(AbstractPaymentData):
    """
    for any response from paypal trying to make a payment
    """
    class Meta:
        abstract = False


