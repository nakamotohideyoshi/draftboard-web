#
# sports/forms.py

from django import forms
from .models import SiteSport

class PlayerCsvForm( forms.Form ):
    """
    Form to select a site sport
    """

    site_sport = forms.ModelChoiceField(queryset=SiteSport.objects.all(),
                                             label='the sport you want to get a player csv for')