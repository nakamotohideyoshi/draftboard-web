
from django.contrib.auth.models import User
from django.db import models
import fpp.classes
from transaction.models import TransactionDetail, Balance

class FppBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    class Meta:
        verbose_name = 'FPP Balance'

class FppTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    class Meta:
        verbose_name = 'FPP Transaction'

class AdminFpp(models.Model):
    """
    keep track of times the admin has deposited cash
    """
    amount  = models.DecimalField( decimal_places=2, max_digits=20, default=0 )
    reason  = models.CharField( max_length=255, default='', null=False, blank=True )
    created = models.DateTimeField(auto_now_add=True, null=True)

    # def __str__(self):
    #     return '+ $%s - %s (%s)' % (self.amount, self.user.username, self.user.email)
    #
    # #
    # # create the FppTransaction
    # def save(self, *args, **kwargs):
    #
    #     if self.pk is None:
    #         t = fpp.classes.FppTransaction( self.user )
    #         t.deposit( self.amount )
    #
    #     super(AdminFppDeposit, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class AdminFppDeposit(AdminFpp):

    user    = models.ForeignKey( User, related_name='adminfppdeposit_user' )

    def __str__(self):
        return '+ %s FPP - %s (%s)' % (self.amount, self.user.username, self.user.email)

    # create the FppTransaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = fpp.classes.FppTransaction( self.user )
            t.deposit( self.amount )
        super(AdminFppDeposit, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Admin Gift'

class AdminFppWithdraw(AdminFpp):

    user    = models.ForeignKey( User, related_name='adminfppwithdraw_user' )

    def __str__(self):
        return '- $%s FPP - %s (%s)' % (self.amount, self.user.username, self.user.email)

    # create the FppTransaction
    def save(self, *args, **kwargs):
        if self.pk is None:
            t = fpp.classes.FppTransaction( self.user )
            t.deposit( self.amount )
        super(AdminFppWithdraw, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Admin Removal'

