from django.views.generic.base import TemplateView


class FrontendHomepageTemplateView(TemplateView):
    template_name = 'frontend/homepage.html'


class FrontendLiveTemplateView(TemplateView):
    template_name = 'frontend/live.html'


class FrontendLayoutTemplateView(TemplateView):
    """
    Shows the fluid layout we will be using
    """
    template_name = 'frontend/layout.html'


class FrontendStyleGuideTemplateView(TemplateView):
    """
    Shows reusable styles for the site
    """
    template_name = 'frontend/styleguide.html'


class FrontendLobbyTemplateView(TemplateView):
    template_name = 'frontend/lobby.html'


class FrontendSettingsTemplateView(TemplateView):
    """
    Build out of settings page. Coderden should take this and incorporate into their backend.
    """
    template_name = 'frontend/settings.html'

class FrontendResultsTemplateView(TemplateView):
    template_name = 'frontend/results.html'


class FrontendSettingsDepositsTemplateView(TemplateView):
    template_name = 'frontend/settings/deposits.html'


class FrontendSettingsTransactionHistoryTemplateView(TemplateView):
    template_name = 'frontend/settings_transactions.html'


class FrontendSettingsWithdrawsTemplateView(TemplateView):
    """
    Build out of settings page. Coderden should take this and incorporate into their backend.
    """
    template_name = 'frontend/settings/withdraws.html'


class FrontendTooltipTemplateView(TemplateView):
    """
    Shows the fluid layout we will be using
    """
    template_name = 'frontend/tooltip.html'


class FrontendDraftTemplateView(TemplateView):
    """
    Draft a team page.
    """
    # TODO: Check if the draft_group_id GET param is for a valid draft group. 404 otherwise.
    template_name = 'frontend/draft.html'


class FrontendPaneTemplateView(TemplateView):
    """
    Right side pane styling and display
    """

    template_name = 'frontend/partials/pane.html'
