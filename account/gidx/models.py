from django.contrib.auth.models import User
from django.db import models
from account.models import Identity
from django.contrib.postgres.fields import JSONField


class GidxSession(models.Model):
    """
    The Session table will store/log each call to a GIDX Platform service and can be used for
    tracking usage, reviewing possible errors, and as a reference to data sent or received from the
    GIDX Platform.

    (http://www.tsevo.com/Docs/MerchantPreparation)
    """
    user = models.ForeignKey(
        User,
        related_name='gidx_sessions'
    )
    gidx_customer_id = models.CharField(
        null=False,
        help_text="The MerchantCustomerID in the GIDX dashboard",
        max_length=256,
    )
    session_id = models.CharField(max_length=128)
    service_type = models.CharField(max_length=128)
    device_location = models.CharField(max_length=128)
    request_data = JSONField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    reason_codes = models.CharField(max_length=128)
    response_data = JSONField(blank=True, null=True)

    class Meta:
        get_latest_by = "created"


class GidxCustomerMonitor(models.Model):
    """
    We have a webhook on our server that listens for Customer Monitor requests from Gidx. These
    contain updates about our customer's identities. We keep track of those updates in this model.

    The CustomerStatus table is recommend as a way to track the progress/changes to a customers
    Identity Verification. In most cases a customers Identity Verification status will not changes
    once they have been marked as "ID-VERIFIED" but there are instances when a customer may have
    their verification status updated based on new identity information, changes to compliance
    laws, etc.

    (http://www.tsevo.com/Docs/MerchantPreparation)
    """
    # Tie to a User.Identity (if one exists)
    identity = models.ForeignKey(
        Identity,
        related_name='gidx_customer_monitors',
        null=True,
        blank=True,
    )
    gidx_customer_id = models.CharField(
        null=False,
        help_text="The MerchantCustomerID in the GIDX dashboard",
        max_length=256,
    )
    reason_codes = models.CharField(max_length=128)
    watch_checks = models.CharField(max_length=128)
    location_detail = models.CharField(max_length=128)
    identity_confidence_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    fraud_confidence_score = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    request_data = JSONField(blank=True, null=True)
