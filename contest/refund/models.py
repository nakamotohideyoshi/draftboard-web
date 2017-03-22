from django.db import models

from ..models import Action, Entry


class Refund(Action):
    # Entry is null-able because if we refund a deregistered entry, the entry is deleted.
    entry = models.OneToOneField(Entry, null=True, on_delete=models.SET_NULL)
    contest_pool = models.ForeignKey('contest.ContestPool', null=False)

    def __str__(self):
        return "<Refund user: %s | id: %s | contest_pool: %s " % (
            self.transaction.user, self.pk, self.contest_pool)
