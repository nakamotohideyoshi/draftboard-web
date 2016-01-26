# cash/models.py

from django.db import models
from django.core.validators import MinValueValidator
from transaction.models import TransactionDetail, Balance
from django.contrib.auth.models import User
import cash.classes
from transaction.models import Transaction, AbstractAmount
import cash.classes

class CashAmount( AbstractAmount ):

    created  = models.DateTimeField(auto_now_add=True, null=True)
    amount   = models.DecimalField(decimal_places=2, max_digits=10)

    def get_category(self):
        return 'cash'

    def get_transaction_class(self):
        """
        return a class with which we can create an instance and make a deposit transaction
        """
        return cash.classes.CashTransaction

    def get_cash_value(self):
        return self.amount

    def __str__(self):
        return '%s | %s' % (self.__class__.__name__, self.amount)

class CashBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    pass

class CashTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    class Meta:
        verbose_name = 'Cash Transaction'

class BraintreeTransaction(models.Model):
    """
    Keeps a record of the Braintree transaction ids in association
    with the DFS internal :class:`transaction.models.Transaction` model.
    """
    transaction             = models.ForeignKey( Transaction )
    braintree_transaction   = models.CharField( max_length=128, null=False )
    created                 = models.DateTimeField(auto_now_add=True, null=True)

class OptimalPaymentsTransaction(models.Model):
    """
    Keeps a record of the Braintree transaction ids in association
    with the DFS internal :class:`transaction.models.Transaction` model.
    """
    transaction             = models.ForeignKey( Transaction )
    netbanx_transaction_id  = models.CharField( max_length=128, null=False,
                                        help_text='netbanx id found in the payment processor account')
    created                 = models.DateTimeField(auto_now_add=True, null=True)

class AdminCashDeposit( models.Model ):
    """
    keep track of times the admin has deposited cash
    """
    user    = models.ForeignKey( User, related_name='admincashdeposit_user' )
    amount  = models.DecimalField( decimal_places=2, max_digits=20, default=0,
                                   validators=[MinValueValidator(0.01)] )
    reason  = models.CharField( max_length=255, default='', null=False, blank=True )

    created = models.DateTimeField(auto_now_add=True, null=True)

    #
    #
    def __str__(self):
        return '+ $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    #
    # create the transaction
    def save(self, *args, **kwargs):

        if self.pk is None:
            t = cash.classes.CashTransaction( self.user )
            t.deposit( self.amount )

        super(AdminCashDeposit, self).save(*args, **kwargs)

class AdminCashWithdrawal( models.Model ):
    """
    keep track of times the admin has withdrawn cash
    """
    user    = models.ForeignKey( User, related_name='admincashwithdrawal_user' )
    amount  = models.DecimalField( decimal_places=2, max_digits=20, default=0,
                                   validators=[MinValueValidator(0.01)] )
    reason  = models.CharField( max_length=255, default='', null=False, blank=True )

    created = models.DateTimeField(auto_now_add=True, null=True)

    #
    #
    def __str__(self):
        return '- $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    #
    # create the transaction
    def save(self, *args, **kwargs):

        if self.pk is None:
            t = cash.classes.CashTransaction( self.user )
            t.withdraw( self.amount )

        super(AdminCashWithdrawal, self).save(*args, **kwargs)

