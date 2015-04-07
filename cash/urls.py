from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView, BalanceAPIView

urlpatterns = patterns('',
    (r'^history/$', TransactionHistoryAPIView.as_view()),
    (r'^balance/$', BalanceAPIView.as_view()),

)

