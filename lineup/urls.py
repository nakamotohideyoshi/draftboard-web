#
# lineup/urls.py

from django.conf.urls import patterns
from lineup.views import (
    UserUpcomingAPIView,
    UserLiveAPIView,
    UserHistoryAPIView,
    PlayersAPIView,
    CreateLineupAPIView,
    EditLineupAPIView,
    LineupUserAPIView,
    EditLineupStatusAPIView,
    EditEntryLineupAPIView,
    EditEntryLineupStatusAPIView,
)

urlpatterns = patterns( '',

    #
    # create a new lineup (it may merge with an existing lineup if its identical)
    (r'^create/$', CreateLineupAPIView.as_view()),

    #
    # edit existing lineup
    (r'^edit/$', EditLineupAPIView.as_view()),
    (r'^edit-status/$', EditLineupStatusAPIView.as_view()),

    #
    # edit entry (ie: edit a lineup that is associated in a contest)
    (r'^edit-entry/$', EditEntryLineupAPIView.as_view()),
    (r'^edit-entry-status/$', EditEntryLineupStatusAPIView.as_view()),

    #
    # get the players for the lineup
    (r'^(?P<pk>[0-9]+)$', PlayersAPIView.as_view()),

    #
    # get a logged in user's upcoming contests
    (r'^upcoming/$', UserUpcomingAPIView.as_view()),

    #
    # get a logged in user's live contests
    (r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    (r'^history/$', UserHistoryAPIView.as_view()),

    #
    # for the given lineup_ids, get the username of the owner
    # LineupUserAPIView
    (r'^usernames/$', LineupUserAPIView.as_view()),
)