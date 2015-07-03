#
# contest/urls.py

from django.conf.urls import patterns
from contest.views import LobbyAPIView, \
                          UserUpcomingAPIView, UserLiveAPIView, UserHistoryAPIView

urlpatterns = patterns( '',

    #
    # get the contests for display on the main contest lobby
    (r'^lobby/$', LobbyAPIView.as_view()),

    #
    # get a logged in user's upcoming contests
    (r'^upcoming/$', UserUpcomingAPIView.as_view()),

    #
    # get a logged in user's live contests
    (r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    (r'^history/$', UserHistoryAPIView.as_view()),
)
