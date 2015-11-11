#
# optimal_payments/urls.py

from django.conf.urls import patterns
from .views import AddPaymentMethodAPIView, PaymentMethodAPIView, \
                    RemovePaymentMethodAPIView, \
                    DepositPaymentTokenAPIView, DepositCreditCardAPIView

urlpatterns = patterns(
    '',

    # add a payment method
    (r'^add/$', AddPaymentMethodAPIView.as_view()),

    # remove a deposit method
    (r'^remove/$', RemovePaymentMethodAPIView.as_view()),

    #
    # make a deposit with a saved payment method
    (r'^deposit/method/$', DepositPaymentTokenAPIView.as_view()),

    #
    # make a deposit with a credit card
    (r'^deposit/cc/$', DepositCreditCardAPIView.as_view()),

    #
    # get a list of the payment methods for this user
    (r'^$', PaymentMethodAPIView.as_view()),

)