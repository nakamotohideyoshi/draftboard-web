from django.utils.timezone import utc
from dateutil.relativedelta import relativedelta
from dateutil import parser
from draftgroup.models import DraftGroup
from django.core.management.base import BaseCommand
from replayer.models import TimeMachine

class Command(BaseCommand):
    """
    This adds the django manage.py command called "generate_timemachines"

    This command creates TimeMachine instances based on date range

    Usage:

        $> ./manage.py generate_timemachines <start "2016-03-15"> <end "2016-03-16">

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py generate_timemachines <start "2016-03-15"> <end "2016-03-16">'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('values', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        generate a test game with questions

        :param args:
        :param options:
        :return:
        """

        values = []
        for x in options['values']:
            values.append( x )

        # move start, end back a day to target draft groups from the day before
        start = parser.parse(values[0]).replace(tzinfo=utc) + relativedelta(hours=+10)
        end = parser.parse(values[1]).replace(tzinfo=utc) + relativedelta(hours=+10)

        print('\nSearching for DraftGroups between %s and %s' % (start, end))

        dgs = DraftGroup.objects.filter( start__gte=start, end__lte=end ).order_by('start')

        print("%s DraftGroups found" % dgs.count())

        for dg in dgs:
            print('Creating TimeMachine for draftgroup: %s' % dg)
            tm = TimeMachine.objects.create(
                replay='Replay for %s' % dg,
                start=dg.start + relativedelta(minutes=-5),
                current=dg.start + relativedelta(minutes=-5),
                target=dg.end + relativedelta(hours=+1),
                playback_mode='play-to-target',
                snapshot_datetime=dg.start + relativedelta(hours=-1)
            )
            tm.save()

            print('TimeMachine #%s created for DraftGroup #%s' % (tm.id, dg))
