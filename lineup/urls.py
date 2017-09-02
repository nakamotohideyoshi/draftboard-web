#
# lineup/urls.py

from django.conf.urls import url
from lineup.views import (
    UserUpcomingAPIView,
    UserLiveAPIView,
    UserCurrentAPIView,
    UserHistoryAPIView,
    PlayersAPIView,
    CreateLineupAPIView,
    EditLineupAPIView,
    LineupUserAPIView,
    EditLineupStatusAPIView,
)

urlpatterns = [

    #
    # create a new lineup (it may merge with an existing lineup if its identical)
    url(r'^create/$', CreateLineupAPIView.as_view()),

    #
    # edit existing lineup
    url(r'^edit/$', EditLineupAPIView.as_view()),
    url(r'^edit-status/(?P<task_id>[a-z0-9-]+)/$', EditLineupStatusAPIView.as_view()),

    #
    # get the players for the lineup
    url(r'^(?P<pk>[0-9]+)$', PlayersAPIView.as_view()),

    #
    # get a logged in user's live & upcoming  contests
    url(r'^current/$', UserCurrentAPIView.as_view()),

    #
    # get a logged in user's upcoming contests
    url(r'^upcoming/$', UserUpcomingAPIView.as_view()),

    #
    # get a logged in user's live contests
    url(r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    url(r'^history/$', UserHistoryAPIView.as_view()),

    #
    # for the given lineup_ids, get the username of the owner
    # LineupUserAPIView
    url(r'^usernames/$', LineupUserAPIView.as_view()),

]
