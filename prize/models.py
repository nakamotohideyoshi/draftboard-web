#
# prize/models.py

from django.db import models

class PrizeStructure( models.Model ):
    """
    Represents a Prize Structure (to which all the actual Prizes can reference,
    and holds the values for the Generator from which it was created from.
    """

    created = models.DateTimeField(auto_now_add=True)

    name            = models.CharField(max_length=128, default='', null=False, blank=True)
    buyin           = models.IntegerField(default=0, null=False)    # label='the amount of the buyin')
    first_place     = models.IntegerField(default=0, null=False)    # label='value ($) of first place as integer')
    round_payouts   = models.IntegerField(default=0, null=False)    # label='each ranks prize must be a multiple of this integer value')
    payout_spots    = models.IntegerField(default=0, null=False)    # total # of prizes
    prize_pool      = models.IntegerField(default=0, null=False)    # total prize pool

    def __str__(self):
        return '< %s | bi: %s, 1st: %s, rnd: %s, spots: %s, pp: %s)' % (
                        self.name,
                        self.buyin, self.first_place, self.round_payouts,
                        self.payout_spots, self.prize_pool)

    #class Meta:
    #   we arent going to make it unique on all 5 things, but we probably should.
    #   there just MAY be a situation in the future where we will want
    #   multiple PrizeStructures with the same values ... no big deal.

class AbstractPrize( models.Model ):
    """
    Abstract parent model which holds generic information about
    the kind of Prize at a specific rank.
    """

    prize_structure = models.ForeignKey( PrizeStructure, null=False )
    rank            = models.IntegerField(default=0, null=False)
    value           = models.FloatField(default=0, null=False)     # float in case of splitting prizes

    def __str__(self):
        return '< rank: %s, value: %s)' % (self.rank, self.value)

    class Meta:
        abstract = True

class AbstractActualPrize( models.Model ):
    """
    Abstract parent model which holds generic information about
    the kind of Prize at a specific rank.
    """

    tied    = models.BooleanField(default=False)

    class Meta:
        abstract = True

class Cash( AbstractPrize ):
    """
    Represents a cash payout at a rank for a PrizeStructure
    """

    class Meta:
        abstract = False # ensure this model gets migrated without any other fields
        unique_together = ('prize_structure','rank')

class Ticket( AbstractPrize ):
    """
    Represents a cash payout at a rank for a PrizeStructure
    """

    class Meta:
        abstract = False # ensure this model gets migrated without any other fields
        unique_together = ('prize_structure','rank')

#
# TODO - having a nice, perfect PrizeStructure is great. We have to have it to do payouts.
#      However -- the actual payouts may include ties which can cause the ACTUAL payouts
#                 to differ from the PrizeStructure. We may want to keep a history
#                 of the actual payouts.
class ActualCash( AbstractActualPrize ):
    """
    Represents a cash payout at a rank for a PrizeStructure
    """

    #tied    = models.BooleanField(default=False)

    class Meta:
        abstract = False # ensure this model gets migrated without any other fields

class ActualTicket( AbstractActualPrize ):
    """
    Represents a cash payout at a rank for a PrizeStructure
    """

    #tied    = models.BooleanField(default=False)

    class Meta:
        abstract = False # ensure this model gets migrated without any other fields