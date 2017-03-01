from django.db import models

from cash.models import CashTransactionDetail
from fpp.models import FppTransactionDetail
from mysite.classes import AbstractManagerClass
from ..models import Action, Entry


class Payout(Action):
    rank = models.PositiveIntegerField(default=0)
    entry = models.OneToOneField(Entry, null=False, related_name='payout')

    def __str__(self):
        return "<Payout user: %s | rank: %s | amount: $%.02f | fp: %.02f | contest: %s>" % (
            self.entry.user, self.rank, self.amount, self.entry.lineup.fantasy_points,
            self.contest.pk)

    @property
    def amount(self):
        ctd = CashTransactionDetail.objects.get(transaction=self.transaction,
                                                user=self.transaction.user)
        return ctd.amount


class Rake(Action):
    def __str__(self):
        return "<Rake user: %s| amount: %s | contest: %s>" % (
            self.transaction.user, self.amount, self.contest)

    @property
    def amount(self):
        ctd = CashTransactionDetail.objects.get(transaction=self.transaction,
                                                user=AbstractManagerClass.get_draftboard_user())
        return ctd.amount


class FPP(Action):
    def __str__(self):
        return "Contest_Name:" + self.contest.name + " username:" + self.transaction.user.username + " ffp: " + str(
            self.amount)

    @property
    def amount(self):
        ctd = FppTransactionDetail.objects.get(transaction=self.transaction,
                                               user=self.transaction.user)
        return ctd.amount
