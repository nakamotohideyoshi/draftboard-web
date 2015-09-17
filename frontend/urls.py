from django.conf.urls import patterns

from frontend import views

urlpatterns = patterns(
    '',
    (r'^frontend/layout/$', views.FrontendLayoutTemplateView.as_view()),
    (r'^frontend/tooltip/$', views.FrontendTooltipTemplateView.as_view()),
    (r'^frontend/live/$', views.FrontendLiveTemplateView.as_view()),
    (r'^frontend/styleguide/$', views.FrontendStyleGuideTemplateView.as_view()),
    (r'^frontend/lobby/$', views.FrontendLobbyTemplateView.as_view()),
    (r'^frontend/settings/$', views.FrontendSettingsTemplateView.as_view()),
    (r'^frontend/settings/transactions/$', views.FrontendSettingsTransactionHistoryTemplateView.as_view()),
    (r'^frontend/settings/deposits/$', views.FrontendSettingsDepositsTemplateView.as_view()),
    (r'^frontend/settings/withdraws/$', views.FrontendSettingsWithdrawsTemplateView.as_view()),
    (r'^draft/$', views.FrontendDraftTemplateView.as_view())
)
