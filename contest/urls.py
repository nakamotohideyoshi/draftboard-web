#
# contest/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from contest.views import LobbyAPIView, AllLineupsView, \
                          UserUpcomingAPIView, UserLiveAPIView, UserHistoryAPIView, \
                          SingleLineupView, CurrentEntryAPIView, SingleContestAPIView, \
                          RegisteredUsersAPIView
from contest.views import ContestCreate, ContestUpdate

urlpatterns = patterns( '',

    url(r'^add/$', ContestCreate.as_view(), name='contest_add'),
    url(r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest-detail'),
    # (r'^add/$', ContestCreate.as_view(), name='contest_add'),
    # (r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest_update'),

    #
    # get the info for a single Contest by its id
    (r'^info/(?P<contest_id>[0-9]+)/$', SingleContestAPIView.as_view()),

    #
    # get a users current entries (the Entries they current have in live/upcoming contests
    (r'^current-entries/$', CurrentEntryAPIView.as_view()),

    #
    # get the contests for display on the main contest lobby
    (r'^lobby/$', LobbyAPIView.as_view()),

    #
    # get a logged in user's upcoming contests
    (r'^upcoming/$', UserUpcomingAPIView.as_view()),

    #
    # get a logged in user's live contests
    (r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    (r'^history/$', UserHistoryAPIView.as_view()),

    #
    # get a single lineup with stats - the lineup can
    # be viewed by any user, and will mask out
    # players who are not yet starting.
    (r'^single-lineup/(?P<contest_id>[0-9]+)/(?P<lineup_id>[0-9]+)$', SingleLineupView.as_view()),

    #
    # get the complete set of specially packed lineups for a contest
    (r'^all-lineups/(?P<contest_id>[0-9]+)$', AllLineupsView.as_view()),

    #
    # get the complete set of specially packed lineups for a contest
    (r'^registered-users/(?P<contest_id>[0-9]+)$', RegisteredUsersAPIView.as_view()),

)

