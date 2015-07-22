from django.db import models
import transaction.models
import transaction.constants
from contest.models import Contest, Entry
class Payout(models.Model):
    created = models.DateTimeField( auto_now_add=True)
    transaction = models.ForeignKey("transaction.Transaction",
                                    null=False)
    contest = models.ForeignKey(Contest)
    entry = models.ForeignKey(Entry)
    rank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Contest_Name:"+self.contest.name+" user_name:"+self.entry.lineup.user.username+"  rank:"+str(self.rank)

