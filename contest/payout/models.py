from django.db import models
from ..models import Action, Entry
from cash.models import CashTransactionDetail
from fpp.models import FppTransactionDetail
from mysite.classes import AbstractManagerClass


class Payout(Action):

    rank = models.PositiveIntegerField(default=0)
    entry = models.OneToOneField(Entry, null=False, related_name='payout' )

    def __str__(self):
        rnk_str     = '(Rank:%s, $%.02f, fp:%.02f)' % (str(self.rank),
                            self.amount, self.entry.lineup.fantasy_points)
        user_str    = self.entry.lineup.user.username
        contest_str = '%s (pk: %s)' % (self.contest.name, self.contest.pk)
        return '%s | %s | %s' % (rnk_str, user_str, contest_str)

    @property
    def amount(self):
        ctd = CashTransactionDetail.objects.get(transaction=self.transaction,
                                                user=self.transaction.user)
        return ctd.amount

class Rake(Action):

    def __str__(self):
        return "Contest_Name:"+self.contest.name+" rake made:"+str(self.amount)

    @property
    def amount(self):
        ctd = CashTransactionDetail.objects.get(transaction=self.transaction,
                                                user=AbstractManagerClass.get_draftboard_user())
        return ctd.amount


class FPP(Action):

    def __str__(self):
        return "Contest_Name:"+self.contest.name+" username:"+self.transaction.user.username + " ffp: "+str(self.amount)

    @property
    def amount(self):
        ctd = FppTransactionDetail.objects.get(transaction=self.transaction,
                                                user=self.transaction.user)
        return ctd.amount


