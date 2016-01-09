#
# sports/urls.py

from django.conf.urls import patterns

from sports.views import (
    PlayerCsvView,
    LeagueInjuryAPIView,
    LeagueTeamAPIView,
    LeaguePlayerAPIView,
    LivePbpView,
    FantasyPointsHistoryAPIView,
    PlayerHistoryAPIView,
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
    # get the teams for a sport
    (r'^players/(?P<sport>[a-z]+)/$', LeaguePlayerAPIView.as_view()),

    #
    # get recent play by play for this draftgroup
    (r'^live-pbp/(?P<sport>[a-z]+)/$', LivePbpView.as_view()),

    #
    # dump the players in a csv format
    (r'^player-csv/$', PlayerCsvView.as_view()),

    #
    # get the fantasy points history for all players
    (r'^fp-history/(?P<sport>[a-z]+)/$', FantasyPointsHistoryAPIView.as_view()),

    #
    # get the player season averages, as well as a 5-game log
    (r'^player-history/(?P<sport>[a-z]+)/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view())

)
