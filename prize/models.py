#
# prize/models.py

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from util.timesince import timesince

class GeneratorSettings( models.Model ):
    buyin           = models.IntegerField(default=0, null=False)    # label='the amount of the buyin')
    first_place     = models.IntegerField(default=0, null=False)    # label='value ($) of first place as integer')
    round_payouts   = models.IntegerField(default=0, null=False)    # label='each ranks prize must be a multiple of this integer value')
    payout_spots    = models.IntegerField(default=0, null=False)    # total # of prizes
    prize_pool      = models.IntegerField(default=0, null=False)    # total prize pool

    def __str__(self):
        return 'buyin: %s, first_place: %s, round_payouts: %s, payout_spots: %s, prize_pool: %s' % \
                (self.buyin, self.first_place, self.round_payouts, self.payout_spots, self.prize_pool)

class PrizeStructure( models.Model ):
    """
    Represents a Prize Structure (to which all the actual Prizes can reference,
    and holds the values for the Generator from which it was created from.
    """

    created = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=128, default='', null=False, blank=True,
                                    help_text='Use a name that will help you remember what the prize structure is for.')

    generator = models.ForeignKey( GeneratorSettings, null=True, blank=True,
                                    help_text='You do not need to specify one of these. But automatically created prize pools may be associated with a generator.')
    buyin = models.DecimalField(decimal_places=2, max_digits=7, default=0)

    def __str__(self):
        return '(%s) %s' % (timesince(self.created), self.name)

class Rank( models.Model ):
    """
    A rank is associated with a specific PrizeStructure and has a
    generic foreign key to an amount model which may represent cash, or ticket prize

    The GFK should always point to a transacation.models.AbstractAmount so
    this models __str__ method works properly, as well
    as the "_____PrizeStructureCreator" classes which build prize structures
    """
    prize_structure = models.ForeignKey( PrizeStructure, null=False )
    rank            = models.IntegerField(default=0, null=False)
    amount_type     = models.ForeignKey(ContentType,
                                         help_text='MUST be a CashAmount or TicketAmount')
    amount_id       = models.IntegerField(help_text='the id of the amount_type field')
    amount          = GenericForeignKey( 'amount_type', 'amount_id' )

    @property
    def value(self):
        """
        wrapper to grab the amount instances 'amount' field ($ value)
        """
        return self.amount.amount

    def __str__(self):
        return '<%s | %s>' % (self.__class__.__name__, self.value)

class CreateTicketPrizeStructure(models.Model):

    created         = models.DateTimeField(auto_now_add=True)
    ticket_value    = models.FloatField(default=0.0, null=False,
                                verbose_name='Ticket Value',
                                help_text='Enter the value of a valid ticket.')
    num_prizes      = models.IntegerField(default=0, null=False,
                                verbose_name='The Number of Total Tickets',
                                help_text='The number of tickets this prize structure should pay out.')
