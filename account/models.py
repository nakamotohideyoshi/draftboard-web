import calendar
import datetime
from logging import getLogger

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

from account import const as _account_const
from account.utils import create_user_log
from cash.classes import CashTransaction

logger = getLogger('account.models')


class Information(models.Model):
    """
    Stores profile information about the user.
    Since we're past the point of being able to create a custom User model by subclassing
    AbstractUser, this is used to store user-related things like permissions and various properties.
    """
    user = models.OneToOneField(User, primary_key=True)
    inactive = models.BooleanField(default=False)
    exclude_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Information'
        verbose_name_plural = "information"
        permissions = (
            ("can_bypass_location_check", "Can bypass location check"),
            ("can_bypass_age_check", "Can bypass age check"),
            ("can_bypass_identity_verification", "Can bypass identity verification"),
            ("email_confirmation", "Email confirmation"),
        )

    @cached_property
    def cash_balance(self):
        """
        Get the user's current cash balance.
        """
        cash_transaction = CashTransaction(self.user)
        return cash_transaction.get_balance_amount()

    @cached_property
    def deposits_limit(self):
        """
        Get the user's deposit limit.
        """
        limits = self.user.limits
        value = 0
        if limits.exists():
            value = self.user.limits.get(type=Limit.DEPOSIT).value
        return value

    @cached_property
    def deposits_for_period(self):
        """
        Get the user's deposits for period of time.
        """
        cash_transaction = CashTransaction(self.user)
        limits = self.user.limits
        deposits = 0
        if limits.exists():
            deposit_limit = self.user.limits.get(type=Limit.DEPOSIT)
            deposits = \
                cash_transaction.get_all_deposits(date_range=deposit_limit.time_period_boundaries)[
                    'amount__sum']
        return deposits

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

    @cached_property
    def is_confirmed(self):
        """
        Check user confirmation status
        """
        confirmed = False
        try:
            confirmed = (self.user.confirmation is not None)
        except ObjectDoesNotExist:
            pass
        return confirmed

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
    user = models.OneToOneField(User, primary_key=True, related_name='identity')
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
    # Is this identity flagged because a similar looking one exists?
    flagged = models.BooleanField(default=False, null=False)

    class Meta:
        verbose_name = 'Trulioo User Identity'
        verbose_name_plural = 'Trulioo User Identities'

    @cached_property
    def state(self):
        # That is issue of zipcode module
        import zipcode
        return zipcode.isequal(self.postal_code).state if zipcode.isequal(
            self.postal_code) else None


class Confirmation(models.Model):
    """
    Option for for checking user confirmation
    """

    user = models.OneToOneField(User, primary_key=True)
    confirmed = models.BooleanField(default=False)


class Limit(models.Model):
    DEPOSIT, ENTRY_ALERT, ENTRY_LIMIT, ENTRY_FEE = range(0, 4)
    TYPES = (
        (DEPOSIT, 'Deposit Limit'),
        (ENTRY_ALERT, 'Contest Entry Alert'),
        (ENTRY_LIMIT, 'Contest Entry Limit'),
        (ENTRY_FEE, 'Entry Fee Limit'),

    )

    MONTHLY, WEEKLY, DAILY = [30, 7, 1]
    PERIODS = (
        (MONTHLY, 'Monthly'),  #
        (WEEKLY, 'Weekly'),
        (DAILY, 'Daily'),

    )
    DEPOSIT_MAX = (
        (50, '$50'),
        (100, '$100'),
        (250, '$250'),
        (500, '$500'),
        (750, '$750'),
        (1000, '$1000'),

    )
    ENTRY_ALERT_MAX = (
        (25, '25'),
        (50, '50'),
        (100, '100'),

    )
    ENTRY_LIMIT_MAX = (
        (50, '50'),
        (100, '100'),
        (250, '250'),
        (500, '500'),

    )
    ENTRY_FEE_MAX = (
        (1, '$1'),
        (2, '$2'),
        (5, '$5'),
        (10, '$10'),
        (25, '$25'),
        (50, '$50'),

    )
    TYPES_GLOBAL = {
        DEPOSIT: {
            "value": DEPOSIT_MAX,
            "time_period": PERIODS
        },
        ENTRY_ALERT: {
            "value": ENTRY_ALERT_MAX,
            "time_period": PERIODS

        },
        ENTRY_LIMIT: {
            "value": ENTRY_LIMIT_MAX,
            "time_period": PERIODS

        },
        ENTRY_FEE: {
            "value": ENTRY_FEE_MAX,
            "time_period": None

        }
    }

    VALUES = [DEPOSIT_MAX, ENTRY_ALERT_MAX, ENTRY_LIMIT_MAX, ENTRY_FEE_MAX]

    user = models.ForeignKey(User, related_name='limits')
    type = models.SmallIntegerField(choices=TYPES)
    value = models.IntegerField(blank=True)
    time_period = models.SmallIntegerField(blank=True, null=True, choices=PERIODS)
    updated = models.DateTimeField(auto_now=True, editable=False)

    @cached_property
    def time_period_boundaries(self):
        month = datetime.datetime.now().month
        year = datetime.datetime.now().year
        time_period = self.time_period
        time_range = []
        if time_period == self.MONTHLY:
            _, num_days = calendar.monthrange(year, month)
            first_day = datetime.date(year, month, 1)
            last_day = datetime.date(year, month, num_days)
            time_range = [first_day, last_day]
        elif time_period == self.WEEKLY:
            today = datetime.date.today()
            current_weekday = today.isoweekday()
            first_day = today - datetime.timedelta(days=current_weekday)
            last_day = first_day + datetime.timedelta(days=6)
            time_range = [first_day, last_day]
        elif time_period == self.DAILY:
            today = datetime.date.today()
            tomorrow = today + datetime.timedelta(days=1)
            time_range = [today, tomorrow]

        return time_range
