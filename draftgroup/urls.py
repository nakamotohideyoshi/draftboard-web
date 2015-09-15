#
# draftgroup/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from draftgroup.views import DraftGroupAPIView, DraftGroupFantasyPointsView

urlpatterns = patterns( '',

    #
    # get the draftgroup players (including the fantasy points for each player currently).
    # use this api to get the fantasy_points for each player in a draftgroup.
    (r'^fantasy-points/(?P<draft_group_id>[0-9]+)$', DraftGroupFantasyPointsView.as_view()),

    #
    # Get the draftgroup players for a draftgroup id.
    # Use this api to get the lists of draftable players for a contest.
    (r'^(?P<pk>[0-9]+)$', DraftGroupAPIView.as_view()),

)