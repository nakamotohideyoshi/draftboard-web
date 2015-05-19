from django.conf.urls import patterns

from .views import TicketAvailableListAPIView

urlpatterns = patterns('',
    (r'^available/$', TicketAvailableListAPIView.as_view()),

)

