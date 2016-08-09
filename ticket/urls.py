from django.conf.urls import url
from .views import (
    TicketAvailableListAPIView,
)

urlpatterns = [
    url(r'^available/$', TicketAvailableListAPIView.as_view()),
]
