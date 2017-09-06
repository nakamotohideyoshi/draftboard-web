from django.conf.urls import url

from cash.withdraw.views import GidxWithdrawCallbackAPIView
from .views import (
    VerifyLocationAPIView,
    UserLimitsAPIView,
    VerifyUserIdentityAPIView,
    AuthAPIView,
    ForgotPasswordAPIView,
    PasswordResetAPIView,
    RegisterAccountAPIView,
    UserAPIView,
    UserCredentialsAPIView,
    UserEmailNotificationAPIView,
    GidxIdentityCallbackAPIView,
    GidxRegistrationStatus,
    GidxDepositAPIView,
    GidxDepositCallbackAPIView,
)

urlpatterns = [

    # registration/authentication
    url(r'^auth/$', AuthAPIView.as_view()),

    url(r'^forgot-password/$', ForgotPasswordAPIView.as_view()),

    url(r'^password-reset-confirm/(?P<uid>.+)/(?P<token>.+)/$', PasswordResetAPIView.as_view()),

    url(r'^register/$', RegisterAccountAPIView.as_view()),

    url(r'^user/$', UserAPIView.as_view()),

    url(r'^settings/$', UserCredentialsAPIView.as_view()),

    url(r'^notifications/email/$', UserEmailNotificationAPIView.as_view()),

    url(r'^verify-location/$', VerifyLocationAPIView.as_view()),

    url(r'^verify-user/$', VerifyUserIdentityAPIView.as_view()),

    url(r'^deposit-form/$', GidxDepositAPIView.as_view()),

    # get a list of user limits
    url(r'^user-limits/$', UserLimitsAPIView.as_view()),

    # GIDX identity callback webhook.
    url(
        r'^identity-webhook/$',
        GidxIdentityCallbackAPIView.as_view(),
        name="gidx-identity-webhook"
    ),

    # GIDX deposit + payout transaction callback webhook.
    url(
        r'^deposit-webhook/$',
        GidxDepositCallbackAPIView.as_view(),
        name="gidx-deposit-webhook"
    ),

    url(
        r'^withdraw-webhook/$',
        GidxWithdrawCallbackAPIView.as_view(),
        name="gidx-withdraw-webhook"
    ),

    # GIDX identity status check.
    url(
        r'^identity-status/(?P<merchant_session_id>.+)/$',
        GidxRegistrationStatus.as_view(),
        name="gidx-identity-status"
    ),

]
