from django.contrib.auth.models import User
from django.db import models

from transaction.models import TransactionDetail, Balance


class RakepaidBalance(Balance):
    """
    Implements the :class:`transaction.models.Balance` model.
    """
    pass


class RakepaidTransactionDetail(TransactionDetail):
    """
    Implements the :class:`transaction.models.TransactionDetail` model.
    """
    pass


class LoyaltyStatus(models.Model):
    name = models.CharField(
        max_length=32,
        default='',
        null=False
    )
    rank = models.IntegerField(
        default=0,
        null=False
    )
    thirty_day_avg = models.FloatField(
        default=0,
        null=False,
        help_text='the minimum required base fpp earned in the last 30 days to achieve this status'
    )
    multiplier = models.FloatField(
        default=1.0,
        null=False
    )

    def __str__(self):
        return '%s(%s) req_30dma: %s, multiplier:%s' % (self.name,
                                                        self.rank, self.thirty_day_avg,
                                                        self.multiplier)


class PlayerTier(models.Model):
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=False)
    status = models.ForeignKey(LoyaltyStatus, null=False)
