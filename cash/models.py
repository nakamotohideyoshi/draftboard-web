# cash/models.py

from django.db import models
from transaction.models import TransactionDetail, Balance
from django.contrib.auth.models import User
import cash.classes

class CashBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    pass

class CashTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    pass

class AdminCashDeposit( models.Model ):
    """
    keep track of times the admin has deposited cash
    """
    user    = models.ForeignKey( User )
    amount  = models.DecimalField( decimal_places=2, max_digits=20, default=0 )
    reason  = models.CharField( max_length=255, default='', null=False, blank=True )

    #
    #
    def __str__(self):
        return '+ $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    #
    # for now as a hack, dont even try to create entries in this table
    def save(self, *args, **kwargs):
        t = cash.classes.CashTransaction( self.user )
        t.deposit( self.amount )

        super(AdminCashDeposit, self).save(*args, **kwargs)

