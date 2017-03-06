#
# urls.py

from django.conf.urls import url
from cash.views import TransactionHistoryAPIView, BalanceAPIView, TransactionDetailAPIView
from cash.withdraw.views import PayPalWithdrawAPIView

urlpatterns = [

    url(r'^transactions/(?P<transaction_id>[0-9]+)/$', TransactionDetailAPIView.as_view()),

    url(r'^transactions/$', TransactionHistoryAPIView.as_view()),

    url(r'^balance/$', BalanceAPIView.as_view()),

    # user can request a withdraw of their funds via check
    # url(r'^withdraw/check/$', CheckWithdrawAPIView.as_view()),

    # user requests withdraw via paypal
    url(r'^withdraw/paypal/$', PayPalWithdrawAPIView.as_view()),

]
