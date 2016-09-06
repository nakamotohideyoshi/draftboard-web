#
# urls.py

from django.conf.urls import url
from .views import (
    PauseActiveReplayAPIView,
    ResumeActiveReplayAPIView,

    ResetReplayAPIView,
)

urlpatterns = [

    # pause the active replay
    url(r'^pause/1/$', PauseActiveReplayAPIView.as_view()),

    # resume the active replay
    url(r'^pause/0/$', ResumeActiveReplayAPIView.as_view()),

    # reset replay
    url(r'^reset-replay/$', ResetReplayAPIView.as_view()),

]