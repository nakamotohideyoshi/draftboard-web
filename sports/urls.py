#
# sports/urls.py

from django.conf.urls import patterns

from sports.views import PlayerCsvView

urlpatterns = patterns(
    '',

    # dump the players in a csv format
    (r'^player-csv/$', PlayerCsvView.as_view())
)