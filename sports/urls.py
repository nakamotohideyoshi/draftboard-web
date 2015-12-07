#
# sports/urls.py

from django.conf.urls import patterns

from sports.views import PlayerCsvView, LeagueInjuryAPIView, LivePbpView, FantasyPointsHistoryAPIView

urlpatterns = patterns(
    '',

    (r'^injuries/(?P<sport>[a-z]+)/$', LeagueInjuryAPIView.as_view()),

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
