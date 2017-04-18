#
# custom command: manage.py testschedule

from django.core.management.base import BaseCommand

from contest.schedule.classes import (
    ScheduleDay,
)


class Command(BaseCommand):
    """
    This seem so simply print out what daily time bocks we have set
    to represent a sport "day". I don't know what it is used for.
    -Zach
    """
    help = "created scheduled contests in the near future"

    def handle(self, *args, **options):
        """
        :param options:
        :return:
        """

        sport = 'nba'
        self.stdout.write('testing ScheduleDay %s...' % sport)
        sd = ScheduleDay(sport, 2015)
        sd.show_time_blocks()
