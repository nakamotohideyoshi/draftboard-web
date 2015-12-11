#
# sports/urls.py

from django.conf.urls import patterns

from sports.views import (
    PlayerCsvView,
    LeagueInjuryAPIView,
    LeagueTeamAPIView,
    LivePbpView,
    FantasyPointsHistoryAPIView
)

urlpatterns = patterns(
    '',

    #
    # get the injruies for a sport
    (r'^injuries/(?P<sport>[a-z]+)/$', LeagueInjuryAPIView.as_view()),

    #
    # get the teams for a sport
    (r'^teams/(?P<sport>[a-z]+)/$', LeagueTeamAPIView.as_view()),

    #
    # get recent play by play for this draftgroup
    (r'^live-pbp/(?P<sport>[a-z]+)/$', LivePbpView.as_view()),

    #
    # dump the players in a csv format
    (r'^player-csv/$', PlayerCsvView.as_view()),

    #
    # get the fantasy points history for all players
    (r'^fp-history/(?P<sport>[a-z]+)/$', FantasyPointsHistoryAPIView.as_view())

)
