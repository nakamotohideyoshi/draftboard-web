from django.conf.urls import patterns

from account.views import RegisterAccountAPIView, UserAPIView,InformationAPIView, UserEmailNotificationAPIView, EmailNotificationAPIView

urlpatterns = patterns('',
    (r'^register/$', RegisterAccountAPIView.as_view()),
    (r'^information/$', InformationAPIView.as_view()),
    (r'^settings/$', UserAPIView.as_view()),
    (r'^email/notification/$', EmailNotificationAPIView.as_view()),
    (r'^email/settings/$', UserEmailNotificationAPIView.as_view()),

)
