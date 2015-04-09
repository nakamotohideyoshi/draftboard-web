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
    user    = models.ForeignKey( User, related_name='admincashdeposit_user' )
    amount  = models.DecimalField( decimal_places=2, max_digits=20, default=0 )
    reason  = models.CharField( max_length=255, default='', null=False, blank=True )

    created = models.DateTimeField(auto_now_add=True, null=True)

    #
    #
    def __str__(self):
        return '+ $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    #
    # for now as a hack, dont even try to create entries in this table
    def save(self, *args, **kwargs):
        request = kwargs.get('request', None )
        if request is None:
            print('request was not passed into the AdminCashDeposit save()')
        else:
            print('request WAS PASSED into the AdminCashDeposit save()')

        if self.pk is None:
            t = cash.classes.CashTransaction( self.user )
            t.deposit( self.amount )

        super(AdminCashDeposit, self).save(*args, **kwargs)

