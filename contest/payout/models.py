from django.db import models
from ..models import Action

class Payout(Action):

    rank = models.PositiveIntegerField(default=0)

    def __str__(self):
        return "Contest_Name:"+self.contest.name+" user_name:"+self.entry.lineup.user.username+"  rank:"+str(self.rank)

