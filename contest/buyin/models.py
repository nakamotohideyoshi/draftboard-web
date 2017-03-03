from django.db import models

from ..models import Action, Entry, ContestPool


class Buyin(Action):
    """
    A buyin is an Action used to keep track of when a user buys into a ContestPool.
    If the entry is not deregistered, and the entry fairmatches into a Contest,
    all fields will stay intact.

    Other possible states are:
        If the user deregisteres (deletes the entry) = null entry field, null contest field
        Entry doesn not get matched into a Contest = null contest field
    """
    # When an entry is removed (due to deregistration or unmatched entry), we still need to know
    # about the buyin, so let this be null.
    entry = models.OneToOneField(Entry, null=True, on_delete=models.SET_NULL)
    # Keep a reference to the contest pool this buyin action was for. We need
    # this because without it, if the entry is not matched into a Contest there
    # would be no way to figure out what the buyin for.
    contest_pool = models.ForeignKey(ContestPool, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        entry_pk = None
        contest_pool_pk = None
        if self.entry:
            entry_pk = self.entry.pk
            contest_pool_pk = self.entry.contest_pool.pk

        return "<Buyin user: %s | entry: %s | contest: %s | contest_pool: %s>" % (
            self.transaction.user, entry_pk, self.contest, contest_pool_pk
        )

    def to_json(self):
        entry_pk = None
        contest_pool = None
        contest_pk = None
        description = None
        if self.entry:
            description = self.entry.contest_pool.name
            entry_pk = self.entry.pk
            contest_pool = {
                "id": self.entry.contest_pool.pk,
                "name": self.entry.contest_pool.name
            }

        if self.contest:
            contest_pk = self.contest.pk

        return {
            "created": str(self.created),
            "entry": entry_pk,
            "description": description,
            "contest": contest_pk,
            "contest_pool": contest_pool,
            "type": "Contest Buyin",
            "id": self.pk
        }
