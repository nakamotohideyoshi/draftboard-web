#
# contest/buyin/models.py

from django.db import models

from ..models import Action, Entry


class Buyin(Action):
    # When an entry is removed (due to deregistration or unmatched entry), we still need to know
    # about the buyin, so let this be null.
    entry = models.OneToOneField(Entry, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        entry_pk = None
        contest_pool_pk = None
        if self.entry:
            entry_pk = self.entry.pk
            contest_pool_pk = self.entry.contest_pool.pk

        return "<Buyin user: %s | entry: %s | contest: %s | contest_pool: %s>" % (
            self.transaction.user, entry_pk, self.contest, contest_pool_pk
        )
