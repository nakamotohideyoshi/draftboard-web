#
# draftgroup/urls.py

from django.conf.urls import url
from draftgroup.views import (
    DraftGroupAPIView,
    DraftGroupFantasyPointsView,
    DraftGroupGameBoxscoresView,
    DraftGroupPbpDescriptionView,
    UpcomingDraftGroupAPIView,
    CurrentDraftGroupAPIView,
    # GameUpdateAPIView,
    # PlayerUpdateAPIView,
    # PlayerAndGameUpdateAPIView,
)

urlpatterns = [
    #
    # get the current draft groups (live, and upcoming)
    url(r'current/$', CurrentDraftGroupAPIView.as_view()),

    #
    # get the upcoming draft groups
    url(r'upcoming/$', UpcomingDraftGroupAPIView.as_view()),

    #
    # get recent play by play for this draftgroup
    url(r'^pbp/(?P<draft_group_id>[0-9]+)/$', DraftGroupPbpDescriptionView.as_view()),

    #
    # get the boxscores for this draft group
    url(r'^boxscores/(?P<draft_group_id>[0-9]+)/$', DraftGroupGameBoxscoresView.as_view()),

    #
    # get the draftgroup players (including the fantasy points for each player currently).
    # use this api to get the fantasy_points for each player in a draftgroup.
    url(r'^fantasy-points/(?P<draft_group_id>[0-9]+)/$', DraftGroupFantasyPointsView.as_view()),

    #
    # get the game updates for draft group by its id
    # url(r'^game-updates/(?P<draft_group_id>[0-9]+)/$', GameUpdateAPIView.as_view()),
    # url(r'^player-updates/(?P<draft_group_id>[0-9]+)/$', PlayerUpdateAPIView.as_view()),

    # get the game and player updates
    # i want to deprecate this API, and move the updates api to the 'sports' app
    # and use it similar to stats, aka: /api/sports/updates/{sport}/
    # url(r'^updates/(?P<draft_group_id>[0-9]+)/$', PlayerAndGameUpdateAPIView.as_view()),

    #
    # Get the draftgroup players for a draftgroup id.
    # Use this api to get the lists of draftable players for a contest.
    url(r'^(?P<pk>[0-9]+)/$', DraftGroupAPIView.as_view()),
]
