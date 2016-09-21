from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import UserLog
from .utils import CheckUserAccess


class LoginForm(AuthenticationForm):

    def clean(self):
        checker = CheckUserAccess(action=UserLog.LOGIN, request=self.request)
        access, msg = checker.check_access
        if not access:
            raise forms.ValidationError(msg)
        return super().clean()