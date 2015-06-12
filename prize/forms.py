#
# prize/forms.py

from django import forms

class PrizeGeneratorForm( forms.Form ):

    buyin           = forms.IntegerField(label='Buyin')         # label='the amount of the buyin')
    first_place     = forms.IntegerField(label='First Place')   # label='value ($) of first place as integer')
    round_payouts   = forms.IntegerField(label='Round Payouts') # label='each ranks prize must be a multiple of this integer value')
    payout_spots    = forms.IntegerField(label='Payout Spots')  # total # of prizes
    prize_pool      = forms.IntegerField(label='Prize Pool')    # total prize pool

    create          = forms.BooleanField(required=False, label='Create This Prize Pool?')

