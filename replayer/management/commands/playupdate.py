#
# replayer/management/commands/playupdate.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from replayer.classes import ReplayManager

class Command(BaseCommand):
    """

    if there are 2 or less parameters the values are assumed to be primary keys

        if there is only 1 param:
            'pk' : play this Update only

        if there are 2 params, they form a range:
            'pk_start'
            'pk_end'

    if there are 3 or more values, the parameters are considered to be:
        'max_objects'
        'ts_start'
        'ts_end'

    if length is 3 and the first value in the list is
      the max number of objects to play thru, and
      assume the next two values are unix timestamps that form a range!
      Note: if the end timestamp is less than or equal to the start timestamp
      we will only play objects with the start timestamp
      so you might use the command $> ./manage.py playupdate 0 1467338190681 0
    """
    USAGE_STR   = './manage.py playupdate UPDATE_ID <optional end update id>'
    USAGE_STR2  = './manage.py playupdate 1467338190681 <optional end ts: 147xxxxxxxxxx> 0'

    # help is a Command inner variable
    help = 'usage: ' + USAGE_STR

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('pk', nargs='+', type=int)

    def handle(self, *args, **options):
        """
        generate a salary pool with a default config

        :param args:
        :param options:
        :return:
        """

        update_pks = []
        for update_pk in options['pk']:
            update_pks.append( update_pk )

        # if there is only one update pk, run it:
        size = len(update_pks)

        # play single Update by its pk
        if len(update_pks) == 1:
            rp = ReplayManager()
            rp.play_single_update( update_pks[0], async=False )

        # play range of Updates by pk
        elif len(update_pks) == 2:

            rp = ReplayManager()
            # truncate chars is how many characters of each object to print out.
            # TODO try using the async mode with multiple tasks to test concurrency
            # TODO if you can get it working in non concurrent mode
            rp.play_range( update_pks[0], update_pks[1], async=False, truncate_chars=99999 )

        # if length is 3 and the first value in the list is
        # the max number of objects to play thru, and
        # assume the next two values are unix timestamps that form a range!
        # Note: if the end timestamp is less than or equal to the start timestamp
        # we will only play objects with the start timestamp
        # so you might use the command $> ./manage.py playupdate 0 1467338190681 0
        elif size == 3:
            max_objects = update_pks[0]
            ts_start = update_pks[1]
            ts_end = update_pks[2]

            if ts_end <= ts_start:
                ts_end = ts_start

            rp = ReplayManager()
            print('ts_start:', ts_start, 'ts_end:', ts_end, 'max_objects:', max_objects)
            rp.play_range_by_ts(ts_start, ts_end, max=max_objects, async=False, truncate_chars=99999)

        else:
            self.stdout.write('you must specify at least one update pk, or two update pks to specify a range')
