#
# lineup/urls.py

from django.conf.urls import patterns
from lineup.views import UserUpcomingAPIView, UserLiveAPIView, \
                            UserHistoryAPIView, PlayersAPIView

urlpatterns = patterns( '',

    #
    # get the players for the lineup
    (r'^players/$', PlayersAPIView.as_view()),

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