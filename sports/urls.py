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
    TsxPlayerNewsAPIView,
    TsxPlayerItemsAPIView,
    PlayerNewsAPIView,
    ScheduleGameBoxscoresView,
)

urlpatterns = patterns( '',

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
    (r'^player/history/(?P<sport>[a-z]+)/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view()),

    # #
    # # get news content for the sport, for all the players
    # (r'^player-news/(?P<sport>[a-z]+)/$', TsxPlayerNewsAPIView.as_view()),

    # #
    # # get the player-news/{sport}/ however do so for a limited range per player
    # # TsxPlayerItemsAPIView
    # (r'^player-items/(?P<sport>[a-z]+)/$', TsxPlayerItemsAPIView.as_view()),

    #
    # both urls below return the same data.
    #   1. the first returns only 1 players news
    #   2. the second takes a bit longer but returns all player news
    (r'^player/news/(?P<sport>[a-z]+)/(?P<player>[0-9]+)/$', PlayerNewsAPIView.as_view()),
    (r'^player/news/(?P<sport>[a-z]+)/$', PlayerNewsAPIView.as_view()),

    #
    # for the day (or for nfl - weekly) games.
    # the data should be formatted similar to the draft-group/boxscores/ for ease of use
    # /api/sports/scoreboard-games/nba/
    (r'^scoreboard-games/(?P<sport>[a-z]+)/$', ScheduleGameBoxscoresView.as_view()),

)
