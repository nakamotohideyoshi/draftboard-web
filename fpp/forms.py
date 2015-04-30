#
# fpp/forms.py

from django import forms
import fpp.models

class AdminFppDepositForm(forms.ModelForm):

    class Meta:
        model = fpp.models.AdminFppDeposit
        fields = ['user','amount','reason']

class AdminFppWithdrawForm(forms.ModelForm):

    class Meta:
        model = fpp.models.AdminFppWithdraw
        fields = ['user','amount','reason']

