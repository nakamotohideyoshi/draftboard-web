#
# sports/trigger.py

from dataden.cache.caches import TriggerCache
from dataden.watcher import Trigger
from sports.parser import DataDenParser

class SportTrigger(Trigger):

    def __init__(self, sport):
        self.sport = sport

        # call super method
        super().__init__()

        # internal debug field to help us print out the triggers the first time only
        self.showed_triggers = False

    def reload_triggers(self):
        """
        override parent method, so we can set only the triggers for this sport
        """

        # sets self.triggers with ALL triggers.
        super().reload_triggers()

        # get only specific triggers models for this sport
        self.triggers = self.triggers.filter(db=self.sport)

        if self.showed_triggers == False:
            self.showed_triggers = True

            # print them to the screen so we know exactly which are about to be used
            for t in self.triggers:
                print('    ', t)
