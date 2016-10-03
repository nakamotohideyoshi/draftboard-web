#
# models.py

from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from account.utils import create_user_log
from account import const as _account_const


class Information(models.Model):
    """
    Stores profile information about the user, like their mailing address, etc
    """

    US_STATES = [('NH','NH'), ('CA','CA'), ('FL','FL')] # TODO - finish adding the rest of available states

    user            = models.OneToOneField( User, primary_key=True  )

    fullname        = models.CharField(max_length=100, null=False, default='')
    address1        = models.CharField(max_length=255, null=False, default='')
    address2        = models.CharField(max_length=255, null=False, default='', blank=True)
    city            = models.CharField(max_length=64, null=False, default='')
    state           = models.CharField(choices=US_STATES, max_length=2,  default='')
    zipcode         = models.CharField(max_length=6, null=False, default='')
    dob             = models.DateField( default=None,  null=True)
    class Meta:
        verbose_name = 'Information'

class EmailNotification(models.Model):
    """
    The Individual Notifications table
    """
    CATEGORIES = [('contest','Contest'), ('campaign','Campaign')]

    category        = models.CharField(choices=CATEGORIES, max_length=100, null=False, default='')
    name            = models.CharField(max_length=100, null=False, default='')
    description     = models.CharField(max_length=255, null=False, default='')
    displayed_text  = models.CharField(max_length=512, null=False, default='',
                        help_text='this text is shown to users')
    default_value   = models.BooleanField( default= True )
    deprecated      = models.BooleanField( default= False )

    class Meta:
        unique_together = ("category", "name")
        verbose_name = 'Email Notification'

class UserEmailNotification(models.Model):
    """
    Options for enabling various email / notifications
    """

    user                = models.ForeignKey( 'auth.User' )
    email_notification  = models.ForeignKey( EmailNotification )
    enabled             = models.BooleanField( default = True )

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
        ('amex','AmericanExpress'),
        ('discover','Discover'),
        ('mastercard','MasterCard'),
        ('visa','Visa'),
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

    Log types and actions are found in account/const.py
    """
    type = models.SmallIntegerField(choices=_account_const.TYPES)
    ip = models.CharField(max_length=15)
    user = models.ForeignKey(User, related_name='logs')
    action = models.SmallIntegerField(choices=_account_const.ACTIONS)
    timestamp = models.DateTimeField(auto_now=True)
    metadata = JSONField(blank=True, null=True)

    class Meta:
        verbose_name = 'User Log'
        verbose_name_plural = 'User Logs'
        ordering = ['-timestamp']


def create_log_entry_when_user_logs_in(sender, user, request, **kwargs):
    """
    Whenever a user logs in, create a UserLog entry.
    """
    create_user_log(
        request,
        _account_const.AUTHENTICATION,
        _account_const.LOGIN
    )
# Attach the signal user_logged_in signal.
user_logged_in.connect(create_log_entry_when_user_logs_in)
