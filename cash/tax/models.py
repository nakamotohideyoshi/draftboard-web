from django.db import models
from django.contrib.auth.models import User


class Tax( models.Model ):
    """
    This class keeps track of all
    """
    user            = models.ForeignKey( User )
    tax_identifier  = models.CharField( max_length=9, null=False )
    created         = models.DateTimeField( auto_now_add=True, null=True)

    class Meta:
        unique_together = ('tax_identifier', 'user')

class TaxForm1099(models.Model):
    """
    a token for whether the tax form/link was sent to the user
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, null=False)
    year = models.IntegerField(null=False)
    sent = models.BooleanField(null=False, default=False)
    net_profit = models.FloatField(null=False, default=0.0)

    class Meta:
        unique_together = ('user', 'year')
