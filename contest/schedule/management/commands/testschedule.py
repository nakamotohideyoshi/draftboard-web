#
# custom command: manage.py schedule

from django.core.management.base import NoArgsCommand
from django.utils import timezone
from datetime import datetime, timedelta
from util.dfsdate import DfsDate
from contest.schedule.classes import (
    ScheduleDay,
)

class Command(NoArgsCommand):

    help = "created scheduled contests in the near future"

    def handle_noargs(self, **options):
        """
        :param options:
        :return:
        """

        sport = 'nba'
        self.stdout.write('testing ScheduleDay %s...' % sport)
        sd = ScheduleDay(sport, 2015)
        sd.show_time_blocks()
