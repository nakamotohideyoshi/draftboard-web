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
    PlayerHistoryMlbHitterAPIView,
    PlayerHistoryMlbPitcherAPIView,
    PlayerHistoryMlbAPIView,
    PbpDebugAPIView,
)

urlpatterns = patterns( '',

    #
    # get the injruies for a sport
    (r'^injuries/nba/$', LeagueInjuryAPIView.as_view(), {"sport": "nba"}),
    (r'^injuries/nfl/$', LeagueInjuryAPIView.as_view(), {"sport": "nfl"}),
    (r'^injuries/nhl/$', LeagueInjuryAPIView.as_view(), {"sport": "nhl"}),
    (r'^injuries/mlb/$', LeagueInjuryAPIView.as_view(), {"sport": "mlb"}),

    #
    # get the teams for a sport
    (r'^teams/nba/$', LeagueTeamAPIView.as_view(), {"sport": "nba"}),
    (r'^teams/nfl/$', LeagueTeamAPIView.as_view(), {"sport": "nfl"}),
    (r'^teams/nhl/$', LeagueTeamAPIView.as_view(), {"sport": "nhl"}),
    (r'^teams/mlb/$', LeagueTeamAPIView.as_view(), {"sport": "mlb"}),

    #
    # get the teams for a sport
    (r'^players/nba/$', LeaguePlayerAPIView.as_view(), {"sport": "nba"}),
    (r'^players/nfl/$', LeaguePlayerAPIView.as_view(), {"sport": "nfl"}),
    (r'^players/nhl/$', LeaguePlayerAPIView.as_view(), {"sport": "nhl"}),
    (r'^players/mlb/$', LeaguePlayerAPIView.as_view(), {"sport": "mlb"}),

    #
    # get recent play by play for this draftgroup
    (r'^live-pbp/nba/$', LivePbpView.as_view(), {"sport": "nba"}),
    (r'^live-pbp/nfl/$', LivePbpView.as_view(), {"sport": "nfl"}),
    (r'^live-pbp/nhl/$', LivePbpView.as_view(), {"sport": "nhl"}),
    (r'^live-pbp/mlb/$', LivePbpView.as_view(), {"sport": "mlb"}),

    #
    # dump the players in a csv format
    (r'^player-csv/$', PlayerCsvView.as_view()),

    #
    # get the fantasy points history for all players
    (r'^fp-history/nba/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nba"}),
    (r'^fp-history/nfl/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nfl"}),
    (r'^fp-history/nhl/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "nhl"}),
    (r'^fp-history/mlb/$', FantasyPointsHistoryAPIView.as_view(), {"sport": "mlb"}),


    # single player
    (r'^player/history/nba/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nba"}),
    # all players
    (r'^player/history/nba/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nba"}),

    # single player
    (r'^player/history/nfl/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nfl"}),
    # all players
    (r'^player/history/nfl/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nfl"}),

    # single player
    (r'^player/history/nhl/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nhl"}),
    # all players
    (r'^player/history/nhl/(?P<n_games_history>[0-9]+)/$', PlayerHistoryAPIView.as_view(), {"sport": "nhl"}),

    # single player - if the player id corresponds to a pitcher returns pitcher stats, else returns hitter stats
    (r'^player/history/mlb/(?P<n_games_history>[0-9]+)/(?P<player>[0-9]+)/$', PlayerHistoryMlbAPIView.as_view(), {"sport": "mlb"}),
    # all players - one call for hitters, one for pitchers...
    (r'^player/history/mlb/hitter/(?P<n_games_history>[0-9]+)/$', PlayerHistoryMlbHitterAPIView.as_view(),  {'sport': 'mlb'}),
    (r'^player/history/mlb/pitcher/(?P<n_games_history>[0-9]+)/$', PlayerHistoryMlbPitcherAPIView.as_view(),  {'sport': 'mlb'}),

    #
    # both urls below return the same data.
    #   1. the first returns only 1 players news
    #   2. the second takes a bit longer but returns all player news
    (r'^player/news/nba/(?P<player>[0-9]+)/$', PlayerNewsAPIView.as_view(), {"sport": "nba"}),
    (r'^player/news/nfl/(?P<player>[0-9]+)/$', PlayerNewsAPIView.as_view(), {"sport": "nfl"}),
    (r'^player/news/nhl/(?P<player>[0-9]+)/$', PlayerNewsAPIView.as_view(), {"sport": "nhl"}),
    (r'^player/news/mlb/(?P<player>[0-9]+)/$', PlayerNewsAPIView.as_view(), {"sport": "mlb"}),

    (r'^player/news/nba/$', PlayerNewsAPIView.as_view(), {"sport": "nba"}),
    (r'^player/news/nfl/$', PlayerNewsAPIView.as_view(), {"sport": "nfl"}),
    (r'^player/news/nhl/$', PlayerNewsAPIView.as_view(), {"sport": "nhl"}),
    (r'^player/news/mlb/$', PlayerNewsAPIView.as_view(), {"sport": "mlb"}),

    #
    # for the day (or for nfl - weekly) games.
    # the data should be formatted similar to the draft-group/boxscores/ for ease of use
    # /api/sports/scoreboard-games/nba/
    (r'^scoreboard-games/nba/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nba"}),
    (r'^scoreboard-games/nfl/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nfl"}),
    (r'^scoreboard-games/nhl/$', ScheduleGameBoxscoresView.as_view(), {"sport": "nhl"}),
    (r'^scoreboard-games/mlb/$', ScheduleGameBoxscoresView.as_view(), {"sport": "mlb"}),

    #
    # debug api for the front to get the timestamp when an PBP object was pushered.
    (r'^pbp-debug/(?P<game_srid>[a-z0-9\-]+)/(?P<srid>[a-z0-9\-]+)/$', PbpDebugAPIView.as_view()),

)
