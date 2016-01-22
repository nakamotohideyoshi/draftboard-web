from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView, BalanceAPIView, DepositView
from cash.withdraw.views import CheckWithdrawAPIView

urlpatterns = patterns('',

    (r'^transactions/(?P<start_ts>[0-9]+)/(?P<end_ts>[0-9]+)/(?P<user_id>[0-9]+)/$', TransactionHistoryAPIView.as_view()),
    (r'^transactions/(?P<start_ts>[0-9]+)/(?P<end_ts>[0-9]+)/$', TransactionHistoryAPIView.as_view()),
    (r'^balance/$', BalanceAPIView.as_view()),

    # this was the paypal deposit url
    #(r'^deposit/$', DepositView.as_view()),

    #
    # user can request a withdraw of their funds via check
    (r'^withdraw/check/$', CheckWithdrawAPIView.as_view()),

)

