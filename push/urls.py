from django.conf.urls import patterns
from django.conf.urls import url

from push import views

urlpatterns = patterns(
    '',
    url(r'^receive/$', views.PusherReceiverTemplateView.as_view()),
    url(r'^send/$', views.PusherSendView.as_view(), name='send'),

    url(r'^webhook1/$', views.Webhook1.as_view()),
)
