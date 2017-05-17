from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone

from .models import Limit, Information


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
        try:
            exclude_date = self.user_cache.information.exclude_date
        # If the user has no Information object, have them contact support.
        except Information.DoesNotExist:
            raise forms.ValidationError(
                "Unable to verify account information. Please contact support")
        if exclude_date and exclude_date > timezone.now().date():
            raise forms.ValidationError(
                "Your user was self-excluded. Please contact support to get more details")
        return cleaned_data


class LimitForm(forms.ModelForm):
    value = forms.ChoiceField(choices=Limit.DEPOSIT_MAX + Limit.ENTRY_FEE_MAX)

    class Meta:
        model = Limit
        fields = ['type', 'value', 'time_period', 'user']


class SelfExclusionForm(forms.ModelForm):
    exclude_date = forms.DateField(required=True)

    class Meta:
        model = Information
        fields = ['exclude_date']
