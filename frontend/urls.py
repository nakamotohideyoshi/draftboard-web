from django.conf.urls import patterns
from django.contrib.auth.decorators import login_required
from frontend import views


urlpatterns = patterns(
    '',
    (r'^$', views.FrontendHomepageTemplateView.as_view()),
    (
        r'^draft/(?P<draft_group_id>[0-9]+)/$',
        login_required(views.FrontendDraftTemplateView.as_view())
    ),
    # need these simply to open the react app to then use redux-simple-router
    (r'^live/lineups/(?P<lineup_id>\d+)/contests/(?P<contest_id>\d+)/$', views.FrontendLiveTemplateView.as_view()),
    (r'^live/lineups/(?P<lineup_id>\d+)/$', views.FrontendLiveTemplateView.as_view()),

    (r'^live/$', views.FrontendLiveTemplateView.as_view()),
    (r'^lobby/$', views.FrontendLobbyTemplateView.as_view()),
    # Contest detail view in lobby.
    (r'^lobby/(?P<contest_id>\d+)/$', views.FrontendLobbyTemplateView.as_view()),
    (r'^results/$', views.FrontendResultsTemplateView.as_view()),
    (r'^settings/$', views.FrontendSettingsTemplateView.as_view()),
    (r'^settings/transactions/$', views.FrontendSettingsTransactionHistoryTemplateView.as_view()),
    (r'^settings/deposits/$', views.FrontendSettingsDepositsTemplateView.as_view()),
    (r'^settings/withdraws/$', views.FrontendSettingsWithdrawsTemplateView.as_view()),
)
