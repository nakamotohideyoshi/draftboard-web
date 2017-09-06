from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

import cash.classes
from contest.models import Action
from mysite.classes import AbstractManagerClass
from transaction.models import (
    TransactionDetail,
    Balance,
    Transaction,
    AbstractAmount
)


class CashAmount(AbstractAmount):
    created = models.DateTimeField(auto_now_add=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=10)

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
    transaction = models.ForeignKey(Transaction)
    braintree_transaction = models.CharField(max_length=128, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)


class GidxTransaction(models.Model):
    """
    Links cash transactions with gidx sessions + merchant transactions so we can
    look them up easily.
    """
    created = models.DateTimeField(
        auto_now_add=True,
        null=True
    )
    transaction = models.ForeignKey(
        Transaction,
        related_name="gidx_transaction"
    )
    merchant_transaction_id = models.CharField(
        max_length=128,
        null=False,
        help_text="The MerchantTransactionID in the GIDX dashboard"
    )

    def __str__(self):
        return '<%s | %s | %s>' % (
            self.__class__.__name__,
            self.transaction.user.username,
            self.transaction.transaction_detail.amount
        )

class PayPalSavedCardTransaction(models.Model):
    """
    for a saved card
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    transaction = models.ForeignKey(Transaction)
    paypal_transaction_id = models.CharField(max_length=128, null=False)


class PayPalCreditCardTransaction(models.Model):
    """
    for processing a regular credit card
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    transaction = models.ForeignKey(Transaction)
    paypal_transaction_id = models.CharField(max_length=128, null=False)


class PayPalTransaction(models.Model):
    """
    for a paypal account payment
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    transaction = models.ForeignKey(Transaction)
    paypal_transaction_id = models.CharField(max_length=128, null=False)


class VZeroTransaction(models.Model):
    """ for paypal vzero transactions like deposits """
    created = models.DateTimeField(auto_now_add=True, null=True)
    transaction = models.ForeignKey(Transaction)
    transaction_identifier = models.CharField(max_length=128, null=False)


class AdminCashDeposit(models.Model):
    """
    keep track of times the admin has deposited cash
    """
    user = models.ForeignKey(User, related_name='admincashdeposit_user')
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0,
                                 validators=[MinValueValidator(0.01)])
    reason = models.CharField(max_length=255, default='', null=False, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True)

    #
    #
    def __str__(self):
        return '+ $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    #
    # create the transaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = cash.classes.CashTransaction(self.user)
            t.deposit(self.amount)

        super(AdminCashDeposit, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Admin Gift"


class AdminCashWithdrawal(models.Model):
    """
    keep track of times the admin has withdrawn cash
    """
    user = models.ForeignKey(User, related_name='admincashwithdrawal_user')
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0,
                                 validators=[MinValueValidator(0.01)])
    reason = models.CharField(max_length=255, default='', null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '- $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)

    # create the transaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = cash.classes.CashTransaction(self.user)
            t.withdraw(self.amount)

        super(AdminCashWithdrawal, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Admin Removal"
