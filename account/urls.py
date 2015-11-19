from django.conf.urls import url


from account.views import (
    RegisterAccountAPIView,
    UserAPIView,
    InformationAPIView,
    UserEmailNotificationAPIView,
    EmailNotificationAPIView,

    AccountSettingsView,
    DepositView,
    WithdrawalView,
    TransactionsView,

    # Dummy API endpoints
    UserBasicAPI,
    UserInformationAPI,
    WithdrawAPI,
    DepositAPI,
    PaymentsAPI,
    AddPaymentMethodAPI,
    RemovePaymentMethodAPI,
    SetDefaultPaymentMethodAPI,
    TransactionsAPI,
    TransactionHistoryAPI
)


urlpatterns = [

    url(r'^register/$', RegisterAccountAPIView.as_view()),
    url(r'^information/$', InformationAPIView.as_view()),
    url(r'^settings/$', UserAPIView.as_view()),
    url(r'^email/notification/$', EmailNotificationAPIView.as_view()),
    url(r'^email/settings/$', UserEmailNotificationAPIView.as_view()),


    url(r'^settings/base/$', AccountSettingsView.as_view(), name='account-settings-base'),
    url(r'^settings/deposits/$', DepositView.as_view(), name='account-settings-deposits'),
    url(r'^settings/withdrawals/$', WithdrawalView.as_view(), name='account-settings-withdrawals'),
    url(r'^settings/transactions/$', TransactionsView.as_view(), name='account-settings-transactions'),


    url(r'^api/account/user/$', UserBasicAPI.as_view()),
    url(r'^api/account/information/$', UserInformationAPI.as_view()),
    url(r'^api/account/payments/$', PaymentsAPI.as_view()),
    url(r'^api/account/payments/add/$', AddPaymentMethodAPI.as_view()),
    url(r'^api/account/payments/deposit/$', DepositAPI.as_view()),
    url(r'^api/account/payments/withdraw/$', WithdrawAPI.as_view()),
    url(r'^api/account/payments/setdefault/$', SetDefaultPaymentMethodAPI.as_view()),
    url(r'^api/account/payments/remove/1/$', RemovePaymentMethodAPI.as_view()),

    url(r'^api/transactions/$', TransactionsAPI.as_view()),
    url(r'^api/transactions/history/$', TransactionHistoryAPI.as_view())

]
