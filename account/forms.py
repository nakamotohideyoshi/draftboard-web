from django.contrib.auth.forms import AuthenticationForm
from django.utils import timezone
from django import forms
from django.conf import settings
from .models import UserLog, Information
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
        exclude_date = self.user_cache.information.exclude_date
        if exclude_date and exclude_date > timezone.now().date():
            raise forms.ValidationError("Your user was self-excluded. Please contact support to get more details")
        return cleaned_data


class SelfExclusionForm(forms.ModelForm):
    exclude_date = forms.DateField(required=True)

    class Meta:
        model = Information
        fields = ['exclude_date']
