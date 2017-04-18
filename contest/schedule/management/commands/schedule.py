from django.core.cache import cache
from django.core.management.base import BaseCommand

from contest.schedule.classes import ScheduleManager

"""
Tested Apr 18, 2017 - this is broken:

    'ScheduleManager' object has no attribute 'print_schedules'
"""


class Command(BaseCommand):
    help = "created scheduled contests in the near future"

    cache_key_lock = 'contest.schedule.classes.ScheduleManager'

    # def add_arguments(self, parser):
    #     # Positional arguments
    #     parser.add_argument('minutes', type=int)
    #     parser.add_argument('sport', nargs='+', type=str)
    #
    # def handle(self, *args, **options):
    #     """
    #     generate a salary pool with a default config
    #
    #     :param args:
    #     :param options:
    #     :return:
    #     """
    #     print( 'making sure scheduled contests are created...')
    #
    #     options_minutes = options['minutes']
    #     options_sports  = options['sport']
    #     print( str(options_minutes) )
    #     print( str(options_sports) )

    def handle(self, *args, **options):
        """

        :param options:
        :return:
        """

        # check the cache for the scheduling lock
        if cache.get(self.cache_key_lock):
            self.stdout.write('***scheduling is already in progress. try again in a minute***')
            return

        # get the the lock so we are the only ones performing the scheduling
        cache.set(self.cache_key_lock, 'working', 60)  # 60 seconds max lock

        #
        # ------------------------------------------------------------
        schedule_manager = ScheduleManager()
        schedule_manager.print_schedules()
        schedule_manager.run()
        # ------------------------------------------------------------

        # relinquish the lock when we are done, or if any error occurred
        cache.delete(self.cache_key_lock)
