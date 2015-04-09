# cash/forms.py

from django import forms
from cash.models import AdminCashDeposit

class AdminCashDepositForm(forms.ModelForm):
    class Meta:
        model = AdminCashDeposit
        fields = ['user','amount','reason']   # these are the fields displayed to the admin