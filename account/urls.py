#
# account/urls.py

from django.conf.urls import url

from account.views import (
    AuthAPIView,
    ForgotPasswordAPIView,
    PasswordResetAPIView,
    RegisterAccountAPIView,
    UserAPIView,
    InformationAPIView,
    UserEmailNotificationAPIView,
)

from .views import (

    # paypal apis:
    PayPalDepositWithPayPalAccountAPIView,              # TODO
    PayPalDepositWithPayPalAccountSuccessAPIView,       # TODO part of flow using paypal account
    PayPalDepositWithPayPalAccountFailAPIView,          # TODO part of flow using paypal account
    PayPalDepositCreditCardAPIView,
    PayPalDepositSavedCardAPIView,
    PayPalSavedCardAddAPIView,
    PayPalSavedCardDeleteAPIView,
    PayPalSavedCardListAPIView,
    SetSavedCardDefaultAPIView,

    # paypal vzero apis
    VZeroGetClientTokenView,
    VZeroDepositView,
)

urlpatterns = [

    # registration/authentication
    url(r'^auth/$', AuthAPIView.as_view()),

    url(r'^forgot-password/$', ForgotPasswordAPIView.as_view()),

    url(r'^password-reset-confirm/(?P<uid>.+)/(?P<token>.+)/$', PasswordResetAPIView.as_view()),

    url(r'^register/$', RegisterAccountAPIView.as_view()),

    url(r'^information/$', InformationAPIView.as_view()),

    url(r'^settings/$', UserAPIView.as_view()),

    url(r'^notifications/email/$', UserEmailNotificationAPIView.as_view()),

    # draftboard apis using paypal apis to move money to/from the site
    # r'^password-reset-confirm/(?P<uid>.+)/(?P<token>.+)/$'

    # TODO - currently unimplemented
    # make a deposit with a paypal account
    url(r'^paypal/deposit/account/$', PayPalDepositWithPayPalAccountAPIView.as_view()),

    # TODO - deposit with paypal success endpoint
    url(r'^paypal/deposit/account/success/$',
        PayPalDepositWithPayPalAccountSuccessAPIView.as_view()),

    # TODO - deposit with paypal failure endpoint
    url(r'^paypal/deposit/account/fail/$', PayPalDepositWithPayPalAccountFailAPIView.as_view()),

    # make a deposit with a credit card
    url(r'^paypal/deposit/cc/$', PayPalDepositCreditCardAPIView.as_view()),

    # make a deposit with a saved payment method
    url(r'^paypal/deposit/saved-card/$', PayPalDepositSavedCardAPIView.as_view()),

    # add a payment method (a saved credit card)
    url(r'^paypal/saved-card/add/$', PayPalSavedCardAddAPIView.as_view()),

    # remove a saved credit card for this user
    url(r'^paypal/saved-card/delete/$', PayPalSavedCardDeleteAPIView.as_view()),

    # get a list of the saved cards
    url(r'^paypal/saved-card/list/$', PayPalSavedCardListAPIView.as_view()),

    # set a specific saved card to be the default using its token
    url(r'^paypal/saved-card/default/$', SetSavedCardDefaultAPIView.as_view()),

    #
    # paypal vzero - get a client token
    url(r'^vzero/client-token/$', VZeroGetClientTokenView.as_view()),

    #
    # paypal vzero - make a deposit with shipping information,
    #                as well as the amount and payment_method_nonce
    url(r'^vzero/deposit/$', VZeroDepositView.as_view()),
]
