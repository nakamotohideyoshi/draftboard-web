from django import forms
from cash.withdraw.models import ReviewPendingWithdraw

class ReviewPendingWithdrawModelForm( forms.ModelForm ):

    class Meta:
        model = ReviewPendingWithdraw

