#
# urls.py

from django.conf.urls import url
from cash.views import TransactionHistoryAPIView, BalanceAPIView
from cash.withdraw.views import (
    CheckWithdrawAPIView,
    PayPalWithdrawAPIView,
)

urlpatterns = [

    url(r'^transactions/(?P<user_id>[0-9]+)/$', TransactionHistoryAPIView.as_view()),

    url(r'^transactions/$', TransactionHistoryAPIView.as_view()),

    url(r'^balance/$', BalanceAPIView.as_view()),

    # user can request a withdraw of their funds via check
    url(r'^withdraw/check/$', CheckWithdrawAPIView.as_view()),

    # user requests withdraw via paypal
    url(r'^withdraw/paypal/$', PayPalWithdrawAPIView.as_view()),

]
