from django.db import models
from django.contrib.auth.models import User


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
    zipcode         = models.CharField(max_length=5, null=False, default='')
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



