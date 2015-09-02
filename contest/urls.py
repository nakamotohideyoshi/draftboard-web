#
# contest/urls.py

from django.conf.urls import patterns
from django.conf.urls import url
from contest.views import LobbyAPIView, AllLineupsView, \
                          UserUpcomingAPIView, UserLiveAPIView, UserHistoryAPIView
#from myapp.views import AuthorCreate, AuthorUpdate, AuthorDelete
from contest.views import ContestCreate, ContestUpdate
urlpatterns = patterns( '',

    url(r'^add/$', ContestCreate.as_view(), name='contest_add'),
    url(r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest-detail'),
    # (r'^add/$', ContestCreate.as_view(), name='contest_add'),
    # (r'^(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest_update'),

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
    # get the complete set of specially packed lineups for a contest
    (r'^all-lineups/$', AllLineupsView.as_view()),
)




# urlpatterns += [
#     # ...
#     url(r'contest/add/$', ContestCreate.as_view(), name='contest_add'),
#     url(r'contest/(?P<pk>[0-9]+)/$', ContestUpdate.as_view(), name='contest_update'),
#     #url(r'contest/(?P<pk>[0-9]+)/delete/$', ContestDelete.as_view(), name='author_delete'),
# ]