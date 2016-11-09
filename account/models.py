from logging import getLogger
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.core.exceptions import ObjectDoesNotExist
from django.utils.functional import cached_property
from account.utils import create_user_log
from account import const as _account_const
from cash.classes import CashTransaction

logger = getLogger('account.models')


class Information(models.Model):
    """
    Stores profile information about the user.
    Since we're past the point of being able to create a custom User model by subclassing
    AbstractUser, this is used to store user-related things like permissions and various properties.
    """
    user = models.OneToOneField(User, primary_key=True)

    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = "information"
        permissions = (
            ("can_bypass_location_check", "Can bypass location check"),
            ("can_bypass_age_check", "Can bypass age check"),
            ("can_bypass_identity_verification", "Can bypass identity verification"),
        )

    @cached_property
    def cash_balance(self):
        """
        Get the user's current cash balance.
        """
        cash_transaction = CashTransaction(self.user)
        return cash_transaction.get_balance_amount()

    @cached_property
    def has_verified_identity(self):
        """
        Has the user verified their identity with Trulioo?
        If so they will have a User.Identity model.
        """
        is_verified = False
        try:
            is_verified = (self.user.identity is not None)
        except ObjectDoesNotExist:
            pass
        return is_verified

    def delete(self):
        """
        Don't allow deleting of this model.
        """
        logger.warning('Deleting a User.information instance is not allowed.')


class EmailNotification(models.Model):
    """
    The Individual Notifications table
    """
    CATEGORIES = [('contest', 'Contest'), ('campaign', 'Campaign')]

    category = models.CharField(choices=CATEGORIES, max_length=100, null=False, default='')
    name = models.CharField(max_length=100, null=False, default='')
    description = models.CharField(max_length=255, null=False, default='')
    displayed_text = models.CharField(max_length=512, null=False, default='',
                                      help_text='this text is shown to users')
    default_value = models.BooleanField(default=True)
    deprecated = models.BooleanField(default=False)

    class Meta:
        unique_together = ("category", "name")
        verbose_name = 'Email Notification'


class UserEmailNotification(models.Model):
    """
    Options for enabling various email / notifications
    """

    user = models.ForeignKey('auth.User')
    email_notification = models.ForeignKey(EmailNotification)
    enabled = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "email_notification")


class SavedCardDetails(models.Model):
    """
    A token for using the credit card, plus last four digits and expiration.

    does NOT store the entire credit card, but rather
    enough brief details to be able to identify the card.
    (ie: "Ending in 1234 expires 11/2016")
    """
    CHOICES = (
        ('amex', 'AmericanExpress'),
        ('discover', 'Discover'),
        ('mastercard', 'MasterCard'),
        ('visa', 'Visa'),
    )

    created = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=256, null=False)
    user = models.ForeignKey('auth.User', null=False)
    type = models.CharField(max_length=32, null=False, choices=CHOICES)
    last_4 = models.CharField(max_length=4, null=False)
    exp_month = models.IntegerField(default=0, null=False)
    exp_year = models.IntegerField(default=0, null=False)
    default = models.BooleanField(default=False, null=False)

    class Meta:
        # make sure a user cant have multiple similar saved cards
        unique_together = ('user', 'token')


class UserLog(models.Model):
    """
    Store user actions for easy access

    Log types and actions are found in account/constants.py
    """
    type = models.SmallIntegerField(choices=_account_const.TYPES)
    ip = models.CharField(max_length=15, blank=True, null=True)
    user = models.ForeignKey(User, related_name='logs')
    action = models.SmallIntegerField(choices=_account_const.ACTIONS)
    timestamp = models.DateTimeField(auto_now=True)
    metadata = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'User Log'
        verbose_name_plural = 'User Logs'
        ordering = ['-timestamp']


def create_log_entry_when_user_logs_in(sender, request, user, **kwargs):
    """
    Whenever a user logs in, create a UserLog entry.
    """
    create_user_log(
        request=request,
        user=user,
        type=_account_const.AUTHENTICATION,
        action=_account_const.LOGIN
    )
# Attach the signal user_logged_in signal.
user_logged_in.connect(create_log_entry_when_user_logs_in)


class Identity(models.Model):
    """
    Stores Trulioo identity information. We need to store this in order to check if someone has
    already 'claimed' an identity. Trulioo provides no mechanism for us to check with their service.
    """
    user = models.OneToOneField(User, primary_key=True)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    # I know it seems dumb to store a date like this, but Trulioo accepts them
    # each as different fields, so I'd rather not have to convert in & out of
    # a dateField.
    birth_day = models.PositiveSmallIntegerField(null=False)
    birth_month = models.PositiveSmallIntegerField(null=False)
    birth_year = models.PositiveSmallIntegerField(null=False)
    # Trulioo calls it a postal code, but it's actually a ZIP code
    postal_code = models.CharField(max_length=16, null=False)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trulioo User Identity'
