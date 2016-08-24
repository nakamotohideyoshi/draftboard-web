#
# commmands.py

from django.utils import timezone
from django.core.management.base import BaseCommand
from replayer.classes import (
    ReplayManager,
)

class Command(BaseCommand):
    """
    uses ReplayManager to find the earliest current model in the Update table
    and sets the time to 2 hours before that Update model's 'ts' datetime
    """

    def handle(self, *args, **options):
        """
        """
        replay_manager = ReplayManager()
        replay_manager.set_time_before_replay_start()
        self.stdout.write('[%s] is now the current time!' % str(timezone.now()))
