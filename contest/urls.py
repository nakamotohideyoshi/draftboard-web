#
# contest/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from contest.views import (
    LobbyAPIView,
    AllLineupsView,
    # UserUpcomingAPIView,
    UserUpcomingContestPoolAPIView,
    UserLiveAPIView,
    UserHistoryAPIView,
    SingleContestLineupView,
    SingleLineupView,
    CurrentEntryAPIView,
    SingleContestAPIView,
    RegisteredUsersAPIView,
    EnterLineupAPIView,
    EnterLineupStatusAPIView,
    PayoutsAPIView,
    EditEntryLineupAPIView,
    EditEntryLineupStatusAPIView,
    RemoveAndRefundEntryAPIView,
    RemoveAndRefundEntryStatusAPIView,
    UserPlayHistoryAPIView,
    ContestRanksAPIView,
    UserUpcomingContestPoolAndLiveContestEntriesAPIView,
)
from contest.views import ContestCreate, ContestUpdate

urlpatterns = patterns(
    '',
    url(r'^add/$', ContestCreate.as_view(), name='contest_add'),

    url(r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest-detail'),
    # (r'^add/$', ContestCreate.as_view(), name='contest_add'),
    # (r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest_update'),

    #
    # "buyin" api - ie: enter a lineup into a contest.
    # This endpoint returns a task id which should
    # be used subsequently to check if the buy was successful.
    (r'^enter-lineup/$', EnterLineupAPIView.as_view()),

    #
    # check if the "buyin" -- that is /api/contest/enter-lineup/ -- was successful
    (r'^enter-lineup-status/(?P<task_id>[a-z0-9-]+)/$', EnterLineupStatusAPIView.as_view()),

    #
    # edit entry (ie: edit a lineup that is associated in a contest)
    (r'^edit-entry/$', EditEntryLineupAPIView.as_view()),
    (r'^edit-entry-status/(?P<task_id>[a-z0-9-]+)/$', EditEntryLineupStatusAPIView.as_view()),

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
    # get a logged in user's contest pool entries in UPCOMING CONTEST POOLS ONLY
    (r'^contest-pools/entries/$', UserUpcomingContestPoolAPIView.as_view()),

    #
    # get the users Entries from Upcoming Contest pools, as well as Entries
    # in "live" Contests (ie: contests which have just been created due
    # to a Contest Pool having started)
    (r'^contest-pools/current-entries/$', UserUpcomingContestPoolAndLiveContestEntriesAPIView.as_view()),

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
    (r'^lineup/(?P<contest_id>[0-9]+)/(?P<lineup_id>[0-9]+)/$', SingleLineupView.as_view()),
    (r'^lineup/(?P<lineup_id>[0-9]+)/$', SingleContestLineupView.as_view()),

    #
    # get the complete set of specially packed lineups for a contest
    (r'^all-lineups/(?P<contest_id>[0-9]+)/$', AllLineupsView.as_view()),

    #
    # get a users Entry history. For each lineup returned
    # has some contest information, and final rank. plus overall stats for the day.
    (r'^play-history/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        UserPlayHistoryAPIView.as_view()),

    #
    # get the usernames for all users who have lineups in the contest
    (r'^registered-users/(?P<contest_id>[0-9]+)/$', RegisteredUsersAPIView.as_view()),

    #
    # get payouts for a contest
    (r'^payouts/(?P<contest_id>[0-9]+)/$', PayoutsAPIView.as_view()),

    #
    # get payouts for a contest
    (r'^final-ranks/(?P<contest_id>[0-9]+)/$', ContestRanksAPIView.as_view()),

    #
    # Request to remove a contest pool Entry, and refund the user
    (r'^unregister-entry/(?P<entry_id>[0-9]+)/$', RemoveAndRefundEntryAPIView.as_view()),
    # Check the status of an unregister request.
    (r'^unregister-entry-status/(?P<task_id>[a-z0-9-]+)/$',
        RemoveAndRefundEntryStatusAPIView.as_view()),
)
