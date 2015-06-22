#
# prize/forms.py

from django import forms
from mysite.forms.util import OrderableFieldForm
from ticket.models import TicketAmount

class PrizeCreatorForm( OrderableFieldForm ):
    """
    You should always subclass this form - its not worthwhile to use it directly.

    Every prize structure creation form has to have the buyin, and a flag
    to indicates whether to actually commit the prize structure
    """

    order = [
        'buyin',
        'create'
    ]

    def __init__(self, *args, **kwargs):
        """
        Super __init__ will perform the ordering if we set self.order = ['field1','field'2, ...]
        """
        super().__init__(*args, **kwargs)

    buyin           = forms.FloatField(label='The amount of the buyin for the contest')
    create          = forms.BooleanField(required=False, label='Create This Prize Pool?')

class FlatCashPrizeCreatorForm( PrizeCreatorForm ):
    """
    Inherits:
        buyin
        create
    """

    order = [
        'buyin',
        'first_place',
        'payout_spots',
        'create'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    first_place     = forms.IntegerField(label='First Place')   # label='value ($) of first place as integer')
    payout_spots    = forms.IntegerField(label='Payout Spots')  # total # of prizes

class PrizeGeneratorForm( FlatCashPrizeCreatorForm ):
    """
    Inherits
        buyin
        create
        first_place
        payout_spots
    """

    order = [
        'buyin',
        'first_place',
        'round_payouts',
        'payout_spots',
        'prize_pool',
        'create'
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    round_payouts   = forms.IntegerField(label='Round Payouts') # label='each ranks prize must be a multiple of this integer value')
    prize_pool      = forms.IntegerField(label='Prize Pool')    # total prize pool

class TicketPrizeCreatorForm( PrizeCreatorForm ):
    """
    Inherits
        buyin
        create
    """

    order = [
        'buyin',
        'ticket_amount',
        'num_prizes',
        'create'
    ]

    ticket_amount   = forms.ModelChoiceField(queryset=TicketAmount.objects.all(),
                                             label='the Ticket prize for each spot')
    num_prizes      = forms.IntegerField(label='The number of prize spots paid')


