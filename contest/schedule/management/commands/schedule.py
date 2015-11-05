#
# custom command: manage.py schedule

from django.core.management.base import NoArgsCommand
from django.core.cache import cache
from contest.schedule.classes import ScheduleManager

class Command(NoArgsCommand):

    help = "listen for dataden mongo updates for currently active triggers"

    cache_key_lock = 'contest.schedule.classes.ScheduleManager'

    def handle_noargs(self, **options):
        """

        :param options:
        :return:
        """

        # check the cache for the scheduling lock
        if cache.get(self.cache_key_lock):
            self.stdout.write('***scheduling is already in progress. try again in a minute***')
            return

        # get the the lock so we are the only ones performing the scheduling
        cache.set(self.cache_key_lock, 'working', 60)    # 60 seconds max lock

        #
        #------------------------------------------------------------
        schedule_manager = ScheduleManager()
        schedule_manager.print_schedules()
        schedule_manager.run()
        #------------------------------------------------------------

        # relinquish the lock when we are done, or if any error occurred
        cache.delete(self.cache_key_lock)