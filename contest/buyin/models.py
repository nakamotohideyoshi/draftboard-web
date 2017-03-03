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
