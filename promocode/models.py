#
# promocode/models.py

from django.db import models
from django.contrib.auth.models import User

#
# I think the best plan, is, instead of having a textbox for a code on the user signup, as well as
# a textbox for a code on the deposit page that we should just use have a text box on the deposit.

class Promotion(models.Model):
    """
    all promotions have a code, which users enter
    """
    created     = models.DateTimeField(auto_now_add=True, null=True)
    enabled     = models.BooleanField(default=True, null=False)
    code        = models.CharField(max_length=16, null=False, default='', unique=True, blank=False)
    description = models.CharField(max_length=20148, null=False, default='', blank=False,
                                    help_text='This text may be displayed on the site.')
    admin_notes = models.CharField(max_length=20148, null=False, default='', blank=False,
                                    help_text='make any internal notes here. dont show this to users')
    expires     = models.DateTimeField()

    class Meta:
        abstract = True

class FirstDeposit( Promotion ):

    max_bonuscash = models.DecimalField( decimal_places=2, max_digits=20, default=0, blank=False,
                help_text='the max amount of bonuscash the site will match, ie: $600')
    fpp_per_bonus_dollar = models.FloatField( default=0, null=False, blank=False,
                help_text='number of FPP (ie:rake) that have to be earned for $1 of bonuscash to convert to real cash.')




