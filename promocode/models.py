#
# promocode/models.py

from django.db import models
from django.contrib.auth.models import User

from transaction.models import Transaction

#
# I think the best plan, is, instead of having a textbox for a code on the user signup, as well as
# a textbox for a code on the deposit page that we should just use have a text box on the deposit.

class Promotion(models.Model):
    """
    the master promotion code information, after the promotion is enabled,
    you shouldnt change any of the information - instead, just make a new Promotion.
    """
    created     = models.DateTimeField(auto_now_add=True, null=True)
    enabled     = models.BooleanField(default=True, null=False)
    code        = models.CharField(max_length=16, null=False, default='', unique=True, blank=False,
                        help_text='the code you want users to enter for the promo, ie: "DFS600"' )

    first_deposit_only = models.BooleanField(default=True, null=False,
                        help_text='should we limit this promotion to ONLY first time depositors?')

    description = models.CharField(max_length=2048, null=False, default='', blank=False,
                                    help_text='This text may be displayed on the site.')
    admin_notes = models.CharField(max_length=2048, null=False, default='', blank=False,
                                    help_text='make any internal notes here. dont show this to users')
    expires     = models.DateTimeField(default=None, null=True, blank=True,
                                    help_text='leave blank if you dont want it to ever expire')

    max_bonuscash = models.DecimalField( decimal_places=2, max_digits=20, default=0, blank=False,
                help_text='the max amount of bonuscash the site will match up to, ie: $600')
    fpp_per_bonus_dollar = models.FloatField( default=0, null=False, blank=False,
                help_text='number of FPP (ie:rake) that have to be earned for $1 of bonuscash to convert to real cash.')

class PromoCode(models.Model):
    """
    keeps a reference to the original/master Promotion, and the add/remove transaction

    """
    created     = models.DateTimeField( auto_now_add=True, null=True )

    user        = models.ForeignKey( User, null=False )
    promotion   = models.ForeignKey( Promotion, null=False )
    transaction = models.ForeignKey( Transaction, null=False )


