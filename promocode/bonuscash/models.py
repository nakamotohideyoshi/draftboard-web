from django.contrib.auth.models import User
from django.db import models

import promocode.bonuscash.classes
from transaction.models import TransactionDetail, Balance, Transaction


class BonusCashBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    pass


class BonusCashTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    #
    # The transaction that triggered bonus cash conversion
    trigger_transaction = models.ForeignKey(Transaction, null=True, default=None, related_name='+')

    pass


class AdminBonusCash(models.Model):
    """
    keep track of times the admin has deposited cash
    """
    amount = models.DecimalField(decimal_places=2, max_digits=20, default=0)
    reason = models.CharField(max_length=255, default='', null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True


class AdminBonusCashDeposit(AdminBonusCash):
    user = models.ForeignKey(User, related_name='adminbonusbashdeposit_user')

    def __str__(self):
        return '+ %s BonusCash - %s (%s)' % (self.amount, self.user.username, self.user.email)

    # create the BonusCashTransaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = promocode.bonuscash.classes.BonusCashTransaction(self.user)
            t.deposit(self.amount)
        super(AdminBonusCashDeposit, self).save(*args, **kwargs)


class AdminBonusCashWithdraw(AdminBonusCash):
    user = models.ForeignKey(User, related_name='adminbonuscashwithdraw_user')

    def __str__(self):
        return '- $%s BonusCash - %s (%s)' % (self.amount, self.user.username, self.user.email)

    # create the BonusCashTransaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = promocode.bonuscash.classes.BonusCashTransaction(self.user)
            t.deposit(self.amount)
        super(AdminBonusCashWithdraw, self).save(*args, **kwargs)
