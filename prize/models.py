from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class GeneratorSettings(models.Model):
    # the amount of the buyin
    buyin = models.FloatField(default=0, null=False)
    # value ($) of first place as integer
    first_place = models.FloatField(default=0, null=False)
    # each ranks prize must be a multiple of this integer value
    round_payouts = models.IntegerField(default=0, null=False)
    # total # of prizes
    payout_spots = models.IntegerField(default=0, null=False)
    # total prize pool
    prize_pool = models.FloatField(default=0, null=False)

    def __str__(self):
        return 'buyin: %s, first_place: %s, round_payouts: %s, payout_spots: %s, prize_pool: %s' % \
               (self.buyin, self.first_place, self.round_payouts, self.payout_spots, self.prize_pool)


class PrizeStructure(models.Model):
    """
    Represents a Prize Structure (to which all the actual Prizes can reference,
    and holds the values for the Generator from which it was created from.
    """
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=128, default='', null=False, blank=True,
                            help_text='Use a name that will help you remember what the prize structure is for.')

    generator = models.ForeignKey(
        GeneratorSettings,
        null=True,
        blank=True,
        help_text=(
            'You do not need to specify one of these. But automatically created prize pools may be associated '
            'with a generator.')
    )

    @property
    def buyin(self):
        # TODO - Accommodate for PrizeStructures without a generator since they are optional.
        if self.generator:
            return self.generator.buyin
        return None

    @property
    def prize_pool(self):
        return self.generator.prize_pool

    @property
    def payout_spots(self):
        return self.generator.payout_spots

    def get_entries(self):
        """
        Get the maximum number of entries allowed in the prize stucture. This is the size of
        a contest that uses this prize structure.
        """
        return int(self.prize_pool / (self.buyin * 0.9))

    def __str__(self):
        return '[%s]entries %s' % (self.get_entries(), self.name)

    def get_format_str(self):
        """
        Get a string that describes the type of prize structure it is.
        The number of total entries, along with information about the prizes in factored.

        For example, returns:
            "H2H"               for 1v1, heads-up games
            "50/50"             for 50/50 formats
            "10-Man Tourney"    for curved prize structures
        """
        max_entrants = self.get_entries()
        payout_spots = self.payout_spots

        if max_entrants == 2:
            return 'H2H'
        elif payout_spots == (max_entrants / 2):
            return '50/50'
        else:
            return 'Tourney'  # '%s-Man Tourney' % max_entrants

    class Meta:
        verbose_name = 'Prize Structure'
        verbose_name_plural = 'Prize Structure'


class Rank(models.Model):
    """
    A rank is associated with a specific PrizeStructure and has a
    generic foreign key to an amount model which may represent cash, or ticket prize

    The GFK should always point to a transacation.models.AbstractAmount so
    this models __str__ method works properly, as well
    as the "_____PrizeStructureCreator" classes which build prize structures
    """
    prize_structure = models.ForeignKey(PrizeStructure, null=False, related_name='ranks')
    rank = models.IntegerField(default=0, null=False)
    amount_type = models.ForeignKey(ContentType,
                                    help_text='MUST be a CashAmount or TicketAmount')
    amount_id = models.IntegerField(help_text='the id of the amount_type field')
    amount = GenericForeignKey('amount_type', 'amount_id')

    @property
    def category(self):
        return self.amount.get_category()

    @property
    def value(self):
        """
        wrapper to grab the amount instances 'amount' field ($ value)
        """
        return float(self.amount.amount)

    def __str__(self):
        return '<%s | %s>' % (self.__class__.__name__, self.value)

    class Meta:
        verbose_name = 'Payout Structure'
        verbose_name_plural = 'Payout Structure'


class CreateTicketPrizeStructure(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    ticket_value = models.FloatField(default=0.0, null=False,
                                     verbose_name='Ticket Value',
                                     help_text='Enter the value of a valid ticket.')
    num_prizes = models.IntegerField(default=0, null=False,
                                     verbose_name='The Number of Total Tickets',
                                     help_text='The number of tickets this prize structure should pay out.')
