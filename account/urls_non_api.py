from django.conf.urls import url
from django.contrib.auth import urls as auth_urls
from django.contrib.auth import views as auth_views
from django.conf.urls import include

from account.views import (

    RegisterView,

    # Dummy API endpoints TO BE REMOVED
    # UserBasicAPI,
    # UserInformationAPI,
    WithdrawAPI,
    DepositAPI,
    PaymentsAPI,
    AddPaymentMethodAPI,
    RemovePaymentMethodAPI,
    SetDefaultPaymentMethodAPI,
)


urlpatterns = [
    # override the default logout view to logout then redirect to login page
    url(r'^logout/$', auth_views.logout_then_login),

    # using all the default django 1.8 auth URLs, see django.contrib.auth.urls.py for more information
    url(r'', include(auth_urls)),

    url(r'^register/', RegisterView.as_view(), name='register'),

    # THE FOLLOWING ARE TO BE REMOVED
    # url(r'^account/api/account/user/$', UserBasicAPI.as_view()),
    # url(r'^account/api/account/information/$', UserInformationAPI.as_view()),
    url(r'^account/api/account/payments/$', PaymentsAPI.as_view()),
    url(r'^account/api/account/payments/add/$', AddPaymentMethodAPI.as_view()),
    url(r'^account/api/account/payments/deposit/$', DepositAPI.as_view()),
    url(r'^account/api/account/payments/withdraw/$', WithdrawAPI.as_view()),
    url(r'^account/api/account/payments/setdefault/$', SetDefaultPaymentMethodAPI.as_view()),
    url(r'^account/api/account/payments/remove/1/$', RemovePaymentMethodAPI.as_view()),
]
