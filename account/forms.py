from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import UserLog
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
