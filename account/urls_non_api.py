from django.conf.urls import url
from django.contrib.auth import urls as auth_urls
from django.contrib.auth import views as auth_views
from django.conf.urls import include

from account.views import (

    AccountSettingsView,
    DepositView,
    WithdrawalView,
    TransactionsView,

    RegisterView,

    # Dummy API endpoints TO BE REMOVED
    UserBasicAPI,
    UserInformationAPI,
    WithdrawAPI,
    DepositAPI,
    PaymentsAPI,
    AddPaymentMethodAPI,
    RemovePaymentMethodAPI,
    SetDefaultPaymentMethodAPI,
    TransactionsAPI,
    TransactionHistoryAPI,
)


urlpatterns = [
    # override the default logout view to logout then redirect to login page
    url(r'^logout/$', auth_views.logout_then_login),

    # using all the default django 1.8 auth URLs, see django.contrib.auth.urls.py for more information
    url(r'', include(auth_urls)),

    url(r'^register/', RegisterView.as_view(), name='register'),

    url(r'^account/settings/base/$', AccountSettingsView.as_view(), name='account-settings-base'),
    url(r'^account/settings/deposits/$', DepositView.as_view(), name='account-settings-deposits'),
    url(r'^account/settings/withdrawals/$', WithdrawalView.as_view(), name='account-settings-withdrawals'),
    url(r'^account/settings/transactions/$', TransactionsView.as_view(), name='account-settings-transactions'),

    # THE FOLLOWING ARE TO BE REMOVED
    url(r'^account/api/account/user/$', UserBasicAPI.as_view()),
    url(r'^account/api/account/information/$', UserInformationAPI.as_view()),
    url(r'^account/api/account/payments/$', PaymentsAPI.as_view()),
    url(r'^account/api/account/payments/add/$', AddPaymentMethodAPI.as_view()),
    url(r'^account/api/account/payments/deposit/$', DepositAPI.as_view()),
    url(r'^account/api/account/payments/withdraw/$', WithdrawAPI.as_view()),
    url(r'^account/api/account/payments/setdefault/$', SetDefaultPaymentMethodAPI.as_view()),
    url(r'^account/api/account/payments/remove/1/$', RemovePaymentMethodAPI.as_view()),

    url(r'^account/api/transactions/$', TransactionsAPI.as_view()),
    url(r'^account/api/transactions/history/$', TransactionHistoryAPI.as_view()),

]
