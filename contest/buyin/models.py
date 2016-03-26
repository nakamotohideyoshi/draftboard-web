#
# contest/buyin/models.py

from ..models import Action, Entry
from django.db import models

class Buyin(Action):

    entry = models.OneToOneField(Entry, null=False)

    def __str__(self):
        return "Buyin Contest_Name:"+self.contest.name+" user_name:"+self.transaction.user.username

