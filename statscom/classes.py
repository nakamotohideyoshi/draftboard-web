#
# classes.py

from util.utctime import UtcTime
import draftgroup.classes
from statscom.models import (
    PlayerLookup,
)

class PlayerUpdateManager(draftgroup.classes.PlayerUpdateManager):
    """
    Swish Analytics own class for injecting PlayerUpdate objects into the backend
    particularly so they show up in /api/draft-group/updates/{draft-group-id}/
    """

    # model class for looking up player -> third party id mappings set by admin
    lookup_model_class = PlayerLookup

    # override. update this third party data and enter it as a PlayerUpdate
    def update(self, stats_update):
        # internally calls super().update(player_srid, *args, **kwargs)
        pass

