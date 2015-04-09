# cash/forms.py

from django import forms
import cash.models

class AdminCashDepositForm(forms.ModelForm):

    class Meta:
        model = cash.models.AdminCashDeposit
        fields = ['user','amount','reason']   # these are the fields displayed to the admin