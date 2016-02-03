#
# prize/management/commands/ticketprizes.py

from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from prize.classes import FlatTicketPrizeStructureCreator
from ticket.classes import TicketManager
from ticket.models import TicketAmount

class Command(BaseCommand):
    """
    This adds the django manage.py command called "ticketprizes"

    This command dumps out possible FlatTicketPrizeStructures

    Usage:

        $> ./manage.py ticketprizes <max_entries>

    """

    # help is a Command inner variable
    help = 'usage: ./manage.py ticketprizes <max_entries>'

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

        max_entries           = float(values[0])
        # ticket_amount   = float(values[1])
        # num_payouts     = int(values[2])
        # entries         = int(values[3])
        # try:
        #     name = ' '.join( values[4:] )
        # except:
        #     name = ''
        #
        # self.stdout.write('%s %s %s name[%s]' % (str(buyin),
        #                         str(ticket_amount), str(num_payouts), str(name)))

        # creator = TicketPrizeStructureCreator(buyin, ticket_amount, num_payouts, entries, name=name)
        # creator.save()


        #
        # print out possible prize structures for Flat Ticket Prize structures
        TicketManager.create_default_ticket_amounts()
        FlatTicketPrizeStructureCreator.print_all( max_entries )
