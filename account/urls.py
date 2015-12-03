from django.conf.urls import url


from account.views import (
    RegisterAccountAPIView,
    UserAPIView,
    InformationAPIView,
    UserEmailNotificationAPIView,
    EmailNotificationAPIView
)


urlpatterns = [

    url(r'^register/$', RegisterAccountAPIView.as_view()),
    url(r'^information/$', InformationAPIView.as_view()),
    url(r'^settings/$', UserAPIView.as_view()),
    url(r'^email/notification/$', EmailNotificationAPIView.as_view()),
    url(r'^email/settings/$', UserEmailNotificationAPIView.as_view()),

]
