#
# prize/forms.py

from django import forms
from ticket.models import TicketAmount

class PrizeGeneratorForm( forms.Form ):

    buyin           = forms.IntegerField(label='Buyin')         # label='the amount of the buyin')
    first_place     = forms.IntegerField(label='First Place')   # label='value ($) of first place as integer')
    round_payouts   = forms.IntegerField(label='Round Payouts') # label='each ranks prize must be a multiple of this integer value')
    payout_spots    = forms.IntegerField(label='Payout Spots')  # total # of prizes
    prize_pool      = forms.IntegerField(label='Prize Pool')    # total prize pool

    create          = forms.BooleanField(required=False, label='Create This Prize Pool?')

class TicketPrizeCreatorForm( forms.Form ):

    ticket_amount   = forms.ModelChoiceField(queryset=TicketAmount.objects.all(),
                                             label='the Ticket prize for each spot')
    #ticket_value    = forms.FloatField(label='Ticket Value (must be a valid Ticket amount')
    num_prizes      = forms.IntegerField(label='The number of prize spots paid')
    buyin           = forms.FloatField(label='The amount of the buyin for the contest')
    create          = forms.BooleanField(required=False, label='Create This Prize Pool?')
