from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from account.views import (
    login,
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
    # django auth views we choose to have
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', auth_views.logout_then_login),
    url(r'^password/reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    url(r'^register/', RegisterView.as_view(), name='register'),

    url(r'^admin/', include(admin.site.urls)),

    # frontend templates, will eventually be separated out
    url(r'', include('frontend.urls', namespace='frontend')),

    # TODO swagger docs should not be on production
    url(r'^docs/', include('rest_framework_swagger.urls')),

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
