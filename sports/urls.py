from django.conf.urls import url

from sports.views import (
    PlayerCsvView,
    LeagueTeamAPIView,
    LeaguePlayerAPIView,
    FantasyPointsHistoryAPIView,
    PlayerHistoryAPIView,
    ScheduleGameBoxscoresView,
    PlayerHistoryMlbHitterAPIView,
    PlayerHistoryMlbPitcherAPIView,
    PlayerHistoryMlbAPIView,
    PbpDebugAPIView,
    UpdateAPIView,
    PlayerRetrieveAPIView,
)

urlpatterns = [
    #
    # get updates for a sport
    url(r'^updates/player/(?P<player_srid>[a-z0-9\-]+)/$', PlayerRetrieveAPIView.as_view()),
    url(r'^player-status/nba/$', UpdateAPIView.as_view(), {"sport": "nba"}),
    url(r'^player-status/nba/$', UpdateAPIView.as_view(), {"sport": "nba"}),
    url(r'^player-status/nfl/$', UpdateAPIView.as_view(), {"sport": "nfl"}),
    url(r'^player-status/nhl/$', UpdateAPIView.as_view(), {"sport": "nhl"}),
    url(r'^player-status/mlb/$', UpdateAPIView.as_view(), {"sport": "mlb"}),

    #
    # get the injruies for a spor
    # TODO: Remove the views for these disabled routes.
    # url(r'^injuries/nba/$', LeagueInjuryAPIView.as_view(), {"sport": "nba"}),
    # url(r'^injuries/nfl/$', LeagueInjuryAPIView.as_view(), {"sport": "nfl"}),
    # url(r'^injuries/nhl/$', LeagueInjuryAPIView.as_view(), {"sport": "nhl"}),
    # url(r'^injuries/mlb/$', LeagueInjuryAPIView.as_view(), {"sport": "mlb"}),

    #
    # get the teams for a sport
    url(r'^teams/nba/$', LeagueTeamAPIView.as_view(), {"sport": "nba"}),
    url(r'^teams/nfl/$', LeagueTeamAPIView.as_view(), {"sport": "nfl"}),
    url(r'^teams/nhl/$', LeagueTeamAPIView.as_view(), {"sport": "nhl"}),
    url(r'^teams/mlb/$', LeagueTeamAPIView.as_view(), {"sport": "mlb"}),

    #
    # get the teams for a sport
    url(r'^players/nba/$', LeaguePlayerAPIView.as_view(), {"sport": "nba"}),
    url(r'^players/nfl/$', LeaguePlayerAPIView.as_view(), {"sport": "nfl"}),
    url(r'^players/nhl/$', LeaguePlayerAPIView.as_view(), {"sport": "nhl"}),
    url(r'^players/mlb/$', LeaguePlayerAPIView.as_view(), {"sport": "mlb"}),

    #
    # dump the players in a csv format
    url(r'^player-csv/$', PlayerCsvView.as_view()),

    #
    # get the fantasy points history for all players
    url(r'^fp-history/nba/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nba"}),
    url(r'^fp-history/nfl/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nfl"}),
    url(r'^fp-history/nhl/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nhl"}),
    url(r'^fp-history/mlb/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "mlb"}),

    # single player
    url(r'^player/history/nba/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$',
        PlayerHistoryAPIView.as_view(), {"sport": "nba"}),
    # all players
    url(r'^player/history/nba/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(),
        {"sport": "nba"}),

    # single player
    url(r'^player/history/nfl/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$',
        PlayerHistoryAPIView.as_view(), {"sport": "nfl"}),
    # all players
    url(r'^player/history/nfl/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(),
        {"sport": "nfl"}),

    # single player
    url(r'^player/history/nhl/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$',
        PlayerHistoryAPIView.as_view(), {"sport": "nhl"}),
    # all players
    url(r'^player/history/nhl/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(),
        {"sport": "nhl"}),

    # single player - if the player id corresponds to a pitcher returns pitcher stats, else returns hitter stats
    url(r'^player/history/mlb/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$',
        PlayerHistoryMlbAPIView.as_view(), {"sport": "mlb"}),
    # all players - one call for hitters, one for pitchers...
    url(r'^player/history/mlb/hitter/(?P<n_games_history>[0-9]+)/$',
        PlayerHistoryMlbHitterAPIView.as_view(), {'sport': 'mlb'}),
    url(r'^player/history/mlb/pitcher/(?P<n_games_history>[0-9]+)/$',
        PlayerHistoryMlbPitcherAPIView.as_view(), {'sport': 'mlb'}),

    #
    # for the day (or for nfl - weekly) games.
    # the data should be formatted similar to the draft-group/boxscores/ for ease of use
    # /api/sports/scoreboard-games/nba/
    url(r'^scoreboard-games/nba/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nba"}),
    url(r'^scoreboard-games/nfl/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nfl"}),
    url(r'^scoreboard-games/nhl/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nhl"}),
    url(r'^scoreboard-games/mlb/$', ScheduleGameBoxscoresView.as_view(), {"sport": "mlb"}),

    #
    # debug api for the front to get the timestamp when an PBP object was pushered.
    url(r'^pbp-debug/(?P<game_srid>[a-z0-9\-]+)/(?P<srid>[a-z0-9\-]+)/$',
        PbpDebugAPIView.as_view()),
]
