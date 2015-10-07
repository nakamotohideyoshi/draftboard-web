#
# sports/urls.py

from django.conf.urls import patterns

from sports.views import PlayerCsvView, LeagueInjuryAPIView

urlpatterns = patterns(
    '',

    (r'^injuries/(?P<sport>[a-z]+)$', LeagueInjuryAPIView.as_view()),


    # dump the players in a csv format
    (r'^player-csv/$', PlayerCsvView.as_view())
)