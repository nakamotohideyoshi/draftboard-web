#
# urls.py

from django.conf.urls import url
from frontend import views

urlpatterns = [

    # home page
    url(r'^$', views.FrontendHomepageTemplateView.as_view()),

    # Draft Page
    url(
        r'^draft/(?P<draft_group_id>\d+)/$',
        views.FrontendDraftTemplateView.as_view()
    ),

    # Copy/edit actions on draft page.
    url(
        r'^draft/(?P<draft_group_id>\d+)/lineup/(?P<lineup_id>\d+)/(?P<action>edit|copy)/$',
        views.FrontendDraftTemplateView.as_view()
    ),

    # need these simply to open the react app to then use redux-simple-router
    url(
        r'^live/(?P<sport>[a-z]+)/lineups/(?P<lineup_id>\d+)/contests/(?P<contest_id>\d+)/opponents/(?P<opponent_lineup_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-opponent-mode'
    ),

    url(
        r'^live/(?P<sport>[a-z]+)/lineups/(?P<lineup_id>\d+)/contests/(?P<contest_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-contest-mode'
    ),

    url(
        r'^live/(?P<sport>[a-z]+)/lineups/(?P<lineup_id>\d+)/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live-lineup-mode'
    ),

    url(
        r'^live/$',
        views.FrontendLiveTemplateView.as_view(),
        name='live'
    ),

    url(
        r'^contests/$',
        views.FrontendLobbyTemplateView.as_view(),
        name='lobby'
    ),

    # Contest detail view in lobby.
    url(r'^contests/(?P<contest_id>\d+)/$', views.FrontendLobbyTemplateView.as_view()),

    url(
        r'^contests/(?P<contest_id>\d+)/$',
        views.FrontendLobbyTemplateView.as_view()
    ),
    url(
        r'^results/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$',
        views.FrontendResultsTemplateView.as_view(),
        name='live-results'
    ),

    url(
        r'^results/live-with-lineups/$',
        views.FrontendResultsTemplateView.as_view(),
        name='live-results'
    ),

    url(
        r'^results/$',
        views.FrontendResultsTemplateView.as_view(),
        name='live-results'
    ),

    url(
        r'^account/settings/$',
        views.FrontendSettingsTemplateView.as_view(),
        name='account-settings'
    ),

    url(
        r'^account/transactions/$',
        views.FrontendSettingsTransactionHistoryTemplateView.as_view(),
        name='account-transactions'
    ),

    url(
        r'^account/deposits/$',
        views.FrontendSettingsDepositsTemplateView.as_view(),
        name='account-deposits'
    ),

    url(
        r'^account/withdraw/$',
        views.FrontendSettingsWithdrawTemplateView.as_view(),
        name='account-withdraw'
    ),

    url(
        r'^account/limits/$',
        views.FrontendSettingsUserLimitsTemplateView.as_view(),
        name='user-limits'
    ),

    # body copy pages
    url(
        r'^terms-conditions/$',
        views.FrontendTermsConditionsTemplateView.as_view(),
        name='terms-conditions'
    ),

    url(
        r'^responsible-play/$',
        views.FrontendResponsiblePlayTemplateView.as_view(),
        name='responsible-play'
    ),

    url(
        r'^privacy-policy/$',
        views.FrontendPrivacyPolicyTemplateView.as_view(),
        name='privacy-policy'
    ),

    url(
        r'^restricted-location/$',
        views.FrontendRestrictedLocationTemplateView.as_view(),
        name='restricted-location'
    ),

    url(
        r'^debug/live-animations/$',
        views.FrontendDebugLiveAnimationsTemplateView.as_view(),
        name='debug-live-animations'
    ),
]
