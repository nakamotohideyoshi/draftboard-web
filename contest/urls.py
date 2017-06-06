from django.conf import settings
from django.conf.urls import url
from django.views.decorators.cache import cache_page

from contest.views import (
    LobbyAPIView,
    AllLineupsView,
    UserUpcomingContestPoolAPIView,
    UserLiveAPIView,
    # UserHistoryAPIView,
    SingleContestLineupView,
    SingleLineupView,
    CurrentEntryAPIView,
    SingleContestAPIView,
    SingleContestPoolAPIView,
    RegisteredUsersAPIView,
    EnterLineupAPIView,
    PayoutsAPIView,
    EntryResultAPIView,
    RemoveAndRefundEntryAPIView,
    UserPlayHistoryAPIView,
    UserPlayHistoryWithCurrentAPIView,
    ContestRanksAPIView,
    UserUpcomingContestPoolAndLiveContestEntriesAPIView,
)

urlpatterns = [
    #
    # "buyin" api - ie: enter a lineup into a contest.
    # This endpoint returns a task id which should
    # be used subsequently to check if the buy was successful.
    url(r'^enter-lineup/$', EnterLineupAPIView.as_view(), name='enter-lineup'),

    #
    # edit entry (ie: edit a lineup that is associated in a contest)
    # url(r'^edit-entry/$', EditEntryLineupAPIView.as_view()),

    #
    # get the info for a single Contest by its id
    url(r'^info/(?P<contest_id>[0-9]+)/$', SingleContestAPIView.as_view()),

    #
    # get the info for a single Contest by its id
    url(r'^info/contest_pool/(?P<contest_pool_id>[0-9]+)/$', SingleContestPoolAPIView.as_view()),

    #
    # get a users current entries (the Entries they current have in live/upcoming contests
    url(r'^current-entries/$', CurrentEntryAPIView.as_view()),

    #
    # get the contests for display on the main contest lobby
    url(r'^lobby/$', LobbyAPIView.as_view()),

    #
    # get a logged in user's contest pool entries in UPCOMING CONTEST POOLS ONLY
    url(r'^contest-pools/entries/$', UserUpcomingContestPoolAPIView.as_view()),

    #
    # get the users Entries from Upcoming Contest pools, as well as Entries
    # in "live" Contests (ie: contests which have just been created due
    # to a Contest Pool having started)
    url(
        r'^contest-pools/current-entries/$',
        UserUpcomingContestPoolAndLiveContestEntriesAPIView.as_view()),

    #
    # get a logged in user's live contests
    url(r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    # url(r'^history/$', UserHistoryAPIView.as_view()),

    #
    # get a single lineup with stats - the lineup can
    # be viewed by any user, and will mask out
    # players who are not yet starting.
    url(r'^lineup/(?P<contest_id>[0-9]+)/(?P<lineup_id>[0-9]+)/$', SingleLineupView.as_view()),
    url(r'^lineup/(?P<lineup_id>[0-9]+)/$', SingleContestLineupView.as_view()),

    #
    # get the complete set of specially packed lineups for a contest
    #    note: we can specify the cache we want to use with the 'cache' argument of cache_view()
    url(
        r'^all-lineups/(?P<contest_id>[0-9]+)/$',
        cache_page(60 * 24, cache=settings.API_CACHE_NAME)(AllLineupsView.as_view())
    ),

    #
    # get a users Entry history. For each lineup returned
    # has some contest information, and final rank. plus overall stats for the day.
    url(r'^play-history/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        UserPlayHistoryAPIView.as_view()),

    # retrieves the historical & live lineups (primarily for frontend results section)
    url(r'^play-history-with-current/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<day>[0-9]+)/$',
        UserPlayHistoryWithCurrentAPIView.as_view()),

    #
    # get the usernames for all users who have lineups in the contest
    url(r'^registered-users/(?P<contest_id>[0-9]+)/$', RegisteredUsersAPIView.as_view()),

    #
    # get payouts for a contest
    url(r'^payouts/(?P<contest_id>[0-9]+)/$', PayoutsAPIView.as_view()),

    #
    # get payouts for a contest
    url(r'^final-ranks/(?P<contest_id>[0-9]+)/$', ContestRanksAPIView.as_view()),

    #
    # Request to remove a contest pool Entry, and refund the user
    url(r'^unregister-entry/(?P<entry_id>[0-9]+)/$', RemoveAndRefundEntryAPIView.as_view()),

    url(r'^entries/(?P<entry_id>[0-9]+)/results/$', EntryResultAPIView.as_view()),
]
