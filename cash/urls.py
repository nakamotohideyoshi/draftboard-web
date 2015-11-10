from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView, BalanceAPIView, DepositView
from cash.withdraw.views import CheckWithdrawAPIView

urlpatterns = patterns('',

    (r'^transactions/$', TransactionHistoryAPIView.as_view()),

    (r'^balance/$', BalanceAPIView.as_view()),

    # this was the paypal deposit url
    #(r'^deposit/$', DepositView.as_view()),

    #
    # user can request a withdraw of their funds via check
    (r'^withdraw/check/$', CheckWithdrawAPIView.as_view()),

)

