#
# fpp/forms.py

from django import forms
import fpp.models

class AdminFppDepositForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = True


    class Meta:
        model = fpp.models.AdminFppDeposit
        fields = ['user','amount','reason']

class AdminFppWithdrawForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            for field in self.fields:
                self.fields[field].widget.attrs['readonly'] = True
                self.fields[field].widget.attrs['disabled'] = True



    class Meta:
        model = fpp.models.AdminFppWithdraw
        fields = ['user','amount','reason']

