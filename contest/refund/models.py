from ..models import Action, Entry
from django.db import models

class Refund(Action):

    entry = models.OneToOneField(Entry, null=False)
    contest_pool = models.ForeignKey('contest.ContestPool', null=False)

    def __str__(self):
        return "Refund Contest_Name:"+self.contest.name+" user_name:"+self.entry.lineup.user.username

