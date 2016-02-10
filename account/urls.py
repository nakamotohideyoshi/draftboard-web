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
    EmailNotificationAPIView,
)


urlpatterns = [

    url(r'^auth/$',             AuthAPIView.as_view()),
    url(r'^forgot-password/$',  ForgotPasswordAPIView.as_view() ),

    url(r'^password-reset-confirm/(?P<uid>.+)/(?P<token>.+)/$', PasswordResetAPIView.as_view()),

    url(r'^register/$',             RegisterAccountAPIView.as_view()),
    url(r'^information/$',          InformationAPIView.as_view()),
    url(r'^settings/$',             UserAPIView.as_view()),
    url(r'^email/notification/$',   EmailNotificationAPIView.as_view()),
    url(r'^email/settings/$',       UserEmailNotificationAPIView.as_view()),

]
