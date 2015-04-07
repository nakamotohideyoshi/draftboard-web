from django.conf.urls import patterns

from cash.views import TransactionHistoryAPIView

urlpatterns = patterns('',
    (r'^history/$', TransactionHistoryAPIView.as_view()),

)

