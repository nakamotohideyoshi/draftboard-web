from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView, BalanceAPIView, DepositView

urlpatterns = patterns('',

    (r'^transactions/$', TransactionHistoryAPIView.as_view()),

    (r'^balance/$', BalanceAPIView.as_view()),

    # this was the paypal deposit url
    #(r'^deposit/$', DepositView.as_view()),

)

