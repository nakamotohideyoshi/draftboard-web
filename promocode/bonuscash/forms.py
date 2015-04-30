#
# promocode.bonuscash.forms.py

from django import forms
import promocode.bonuscash.models

class AdminBonusCashDepositForm(forms.ModelForm):

    class Meta:
        model = promocode.bonuscash.models.AdminBonusCashDeposit
        fields = ['user','amount','reason']

class AdminBonusCashWithdrawForm(forms.ModelForm):

    class Meta:
        model = promocode.bonuscash.models.AdminBonusCashWithdraw
        fields = ['user','amount','reason']
