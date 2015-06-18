#
# prize/models.py

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from transaction.models import AbstractAmount
from cash.classes import CashTransaction

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
    name    = models.CharField(max_length=128, default='', null=False, blank=True)

    generator = models.ForeignKey( GeneratorSettings, null=True )

    def __str__(self):
        return '%s %s' % (self.__class__.__name__, self.name)

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
    amount_type     = models.ForeignKey(ContentType)
    amount_id       = models.IntegerField()
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
                                verbose_name='Ticket Value')
    num_prizes      = models.IntegerField(default=0, null=False,
                                verbose_name='The Number of Total Tickets')