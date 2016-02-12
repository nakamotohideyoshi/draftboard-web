from django.conf.urls import patterns
from django.conf.urls import url
from frontend import views


urlpatterns = patterns(
    '',
    (r'^$', views.FrontendHomepageTemplateView.as_view()),
    # Draft Page
    (
        r'^draft/(?P<draft_group_id>\d+)/$',
        views.FrontendDraftTemplateView.as_view()
    ),
    # Copy/edit actions on draft page.
    (
        r'^draft/(?P<draft_group_id>\d+)/lineup/(?P<lineup_id>\d+)/(?P<action>edit|copy)/$',
        views.FrontendDraftTemplateView.as_view()
    ),
    # need these simply to open the react app to then use redux-simple-router
    url(
        r'^live/lineups/(?P<lineup_id>\d+)/contests/(?P<contest_id>\d+)/opponents/(?P<opponent_lineup_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-opponent-mode'
    ),
    url(
        r'^live/lineups/(?P<lineup_id>\d+)/contests/(?P<contest_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-contest-mode'
    ),
    url(
        r'^live/lineups/(?P<lineup_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-lineup-mode'
    ),
    url(
        r'^live/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live'
    ),
    (r'^lobby/$', views.FrontendLobbyTemplateView.as_view()),
    # Contest detail view in lobby.
    (r'^lobby/(?P<contest_id>\d+)/$', views.FrontendLobbyTemplateView.as_view()),
    url(
        r'^results/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.FrontendResultsTemplateView.as_view(),
        name='live-results'
    ),
    url(
        r'^results/$',
        views.FrontendResultsTemplateView.as_view(),
        name='live-results'
    ),
    (r'^settings/$', views.FrontendSettingsTemplateView.as_view()),
    (r'^settings/transactions/$', views.FrontendSettingsTransactionHistoryTemplateView.as_view()),
    (r'^settings/deposits/$', views.FrontendSettingsDepositsTemplateView.as_view()),
    (r'^settings/withdraws/$', views.FrontendSettingsWithdrawsTemplateView.as_view())
)
