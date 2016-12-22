from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import UserLog, Limit
from .utils import CheckUserAccess
from account.utils import create_user_log


class LoginForm(AuthenticationForm):

    def clean(self):
        cleaned_data = super().clean()
        # This is disabled because users CAN login, even with a restricted IP.
        #
        # checker = CheckUserAccess(
        #   action=UserLog.LOGIN, request=self.request, user=self.user_cache)
        # access, msg = checker.check_access
        # if not access:
        #     raise forms.ValidationError(msg)
        return cleaned_data


class LimitForm(forms.ModelForm):
    value = forms.ChoiceField(choices=Limit.DEPOSIT_MAX+Limit.ENTRY_FEE_MAX)

    class Meta:
        model = Limit
        fields = ['type', 'value', 'time_period', 'user']
