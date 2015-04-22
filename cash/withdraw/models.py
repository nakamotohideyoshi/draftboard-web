from django.db import models
from cash.models import CashTransactionDetail

class WithdrawStatus( models.Model ):
    """
    The class that keeps a list of all the statuses
    their corresponding string representation.
    """
    category    = models.CharField(max_length=100, null=False)
    name        = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return '%s  %s' % (self.category, self.name)

class Withdraw(models.Model):
    """
    Abstract implementation fo the withdraw
    """
    created                 = models.DateTimeField(auto_now_add=True, null=True)
    cash_transaction_detail = models.OneToOneField( CashTransactionDetail , null=False )
    status                  = models.ForeignKey( WithdrawStatus, null=False )
    status_updated          = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class PayPalWithdraw(Withdraw):
    email               = models.EmailField(null=False)
    paypal_transaction  = models.CharField( max_length=255, null=False )


class CheckWithdraw(Withdraw):
    US_STATES = [('NH','NH'), ('CA','CA'), ('FL','FL')] # TODO - finish adding the rest of available states

    check_number    = models.IntegerField(null=True, unique=True )
    fullname        = models.CharField(max_length=100, null=False, default='')
    address1        = models.CharField(max_length=255, null=False, default='')
    address2        = models.CharField(max_length=255, null=False, default='')
    city            = models.CharField(max_length=64, null=False, default='')
    state           = models.CharField(choices=US_STATES, max_length=2,  default='')
    zipcode         = models.CharField(max_length=5, null=False, default='')


class ReviewWithdraw(Withdraw):
    email               = models.EmailField(null=False)
    paypal_transaction  = models.CharField( max_length=255, null=False )

    US_STATES = [('NH','NH'), ('CA','CA'), ('FL','FL')] # TODO - finish adding the rest of available states

    check_number    = models.IntegerField(null=True, unique=True )
    fullname        = models.CharField(max_length=100, null=False, default='')
    address1        = models.CharField(max_length=255, null=False, default='')
    address2        = models.CharField(max_length=255, null=False, default='')
    city            = models.CharField(max_length=64, null=False, default='')
    state           = models.CharField(choices=US_STATES, max_length=2,  default='')
    zipcode         = models.CharField(max_length=5, null=False, default='')
