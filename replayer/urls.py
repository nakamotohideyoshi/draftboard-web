#
# urls.py

from django.conf.urls import url
from .views import (
    PauseActiveReplayAPIView,
    ResumeActiveReplayAPIView,

    ResetReplayAPIView,
    FastForwardAPIView,
)

urlpatterns = [

    # pause the active replay
    url(r'^pause/1/$', PauseActiveReplayAPIView.as_view()),

    # resume the active replay
    url(r'^pause/0/$', ResumeActiveReplayAPIView.as_view()),

    # fast-forward url for setting the playback speed
    url(r'^fast-forward/(?P<speed>[0-9]+)/$', FastForwardAPIView.as_view()),

    # reset replay
    url(r'^reset-replay/$', ResetReplayAPIView.as_view()),

]