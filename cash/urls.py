from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView, BalanceAPIView, DepositView

urlpatterns = patterns('',
    (r'^history/$', TransactionHistoryAPIView.as_view()),
    (r'^balance/$', BalanceAPIView.as_view()),
    (r'^deposit/$', DepositView.as_view()),

)

