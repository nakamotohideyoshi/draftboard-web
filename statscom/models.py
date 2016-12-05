from draftgroup.models import AbstractPlayerLookup


class PlayerLookup(AbstractPlayerLookup):
    """
    the admin will be able to set up a draftboard Player and their STATS.com api's id
    so that we can map the swish player to the draftboard player.
    """
    class Meta:
        abstract = False
        ordering = ('last_name', 'first_name', 'created')
