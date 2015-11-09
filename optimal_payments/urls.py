#
# optimal_payments/urls.py

from django.conf.urls import patterns
from .views import AddPaymentMethodAPIView, PaymentMethodAPIView, \
                    RemovePaymentMethodAPIView

urlpatterns = patterns(
    '',

    # add a payment method
    (r'^add/$', AddPaymentMethodAPIView.as_view()),

    #
    (r'^remove/$', RemovePaymentMethodAPIView.as_view()),

    # get a list of the payment methods for this user
    (r'^$', PaymentMethodAPIView.as_view()),

)