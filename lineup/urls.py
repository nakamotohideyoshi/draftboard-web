#
# lineup/urls.py

from django.conf.urls import patterns
#from lineup.views import #ContestLineupsAPIView, \
from lineup.views import UserUpcomingAPIView, UserLiveAPIView, UserHistoryAPIView # not to be confused with contest.views by similar names

urlpatterns = patterns( '',

    #
    # the lineups for a contest. do not display roster information
    # for contests which have not started yet!
    #(r'^contest/$', ContestLineupsAPIView.as_view()),

    #
    # get a logged in user's upcoming contests
    (r'^upcoming/$', UserUpcomingAPIView.as_view()),

    #
    # get a logged in user's live contests
    (r'^live/$', UserLiveAPIView.as_view()),

    #
    # get a logged in user's historical contests
    (r'^history/$', UserHistoryAPIView.as_view()),
)