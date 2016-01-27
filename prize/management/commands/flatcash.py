#
# prize/management/commands/ticketprizes.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from prize.classes import FlatCashPrizeStructureCreator

class Command(BaseCommand):
    """
    This adds the django manage.py command called "ticketprizes"

    This command creates a ticket prize structure using the params from the commd line

    Usage:

        $> ./manage.py ticketprizes <buyin> <ticketAmount> <numPayouts> <optionalName>

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py ticketprizes <buyin> <cashPayoutAmountPerSpot> <numPayouts> <optionalName>'

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

        buyin           = float(values[0])
        ticket_amount   = float(values[1])
        num_payouts     = int(values[2])
        try:
            name = ' '.join( values[3:] )
        except:
            name = ''

        self.stdout.write('%s %s %s name[%s]' % (str(buyin),
                                str(ticket_amount), str(num_payouts), str(name)))
        creator = FlatCashPrizeStructureCreator(buyin, ticket_amount, num_payouts, name=name)
        creator.save()