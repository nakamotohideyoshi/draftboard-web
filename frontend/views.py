from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView


class FrontendHomepageTemplateView(TemplateView):
    template_name = 'frontend/homepage.html'


class FrontendLiveTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/live.html'


class FrontendLobbyTemplateView(TemplateView):
    template_name = 'frontend/lobby.html'


class FrontendSettingsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Build out of settings page. Coderden should take this and incorporate into their backend.
    """
    template_name = 'frontend/settings.html'


class FrontendResultsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/results.html'


class FrontendSettingsDepositsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/settings/deposits.html'


class FrontendSettingsTransactionHistoryTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/settings/transactions.html'


class FrontendSettingsWithdrawsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Build out of settings page. Coderden should take this and incorporate into their backend.
    """
    template_name = 'frontend/settings/withdraws.html'


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
