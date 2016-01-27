# cash/forms.py

from django import forms
import cash.models

class AdminCashDepositForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = True


    class Meta:
        model = cash.models.AdminCashDeposit
        fields = ['user','amount','reason']   # these are the fields displayed to the admin

class DepositAmountForm(forms.Form):
    amount = forms.DecimalField(max_digits=8, decimal_places=2, min_value=10.00,required=True)


class AdminCashWithdrawalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = True


    class Meta:
        model = cash.models.AdminCashWithdrawal
        fields = ['user','amount','reason']   # these are the fields displayed to the admin

