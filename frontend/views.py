from braces.views import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

from contest.models import (
    Entry,
    CurrentContest,
    UpcomingContestPool,
)


class FrontendHomepageTemplateView(TemplateView):
    template_name = 'frontend/homepage.html'

    # If a logged-in user goes to the homepage, redirect them to the lobby.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('frontend:lobby'))

        return super(FrontendHomepageTemplateView, self).get(request, *args, **kwargs)


class FrontendLiveTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'frontend/live.html'

    def get(self, request, *args, **kwargs):
        """
        if a user can be found via the 'user_id' return it,
        else return None.
        """
        contests = CurrentContest.objects.all()
        entries = Entry.objects.filter(lineup__user=request.user, contest__in=contests)

        # if lineup id is not related to user, then redirect to live base url
        lineup_id = kwargs['lineup_id'] if 'lineup_id' in kwargs else None
        if lineup_id:
            if entries.filter(lineup__pk=lineup_id).count() == 0:
                return HttpResponseRedirect(reverse('frontend:live'))

        # if user is not in contest, then redirect back to the lineup mode
        contest_id = kwargs['contest_id'] if 'contest_id' in kwargs else None
        if contest_id:
            if entries.filter(contest__pk=contest_id).count() == 0:
                return HttpResponseRedirect(reverse('frontend:live-lineup-mode', kwargs={
                    'lineup_id': lineup_id,
                }))

            contest = contests.filter(pk=contest_id)[0]

        # if opponent is not in the contest, then redirect back to contest mode
        opponent_lineup_id = kwargs['opponent_lineup_id'] if 'opponent_lineup_id' in kwargs else None
        if opponent_lineup_id:
            # if 1 then we know it's the villian watch
            if opponent_lineup_id is not '1' and Entry.objects.filter(contest__id=contest_id, lineup__pk=opponent_lineup_id).count() == 0:
                return HttpResponseRedirect(reverse('frontend:live-contest-mode', kwargs={
                    'lineup_id': lineup_id,
                    'contest_id': contest_id
                }))

        return super(FrontendLiveTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FrontendLiveTemplateView, self).get_context_data(**kwargs)

        log_level = self.request.GET.get('loglevel', None)
        if log_level in ['trace', 'debug', 'info', 'warn', 'error']:
            context['loglevel'] = log_level

        if self.request.GET.get('wipe_localstorage', 0) is '1':
            context['wipe_localstorage'] = 1

        return context


class FrontendLobbyTemplateView(TemplateView):
    template_name = 'frontend/lobby.html'

    def get_context_data(self, **kwargs):
        context = super(FrontendLobbyTemplateView, self).get_context_data(**kwargs)

        log_level = self.request.GET.get('loglevel', None)
        if log_level in ['trace', 'debug', 'info', 'warn', 'error']:
            context['loglevel'] = log_level

        return context


class FrontendSettingsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Account settings page
    """
    template_name = 'frontend/account/partials/settings.html'


class FrontendSettingsTransactionHistoryTemplateView(LoginRequiredMixin, TemplateView):
    """
    Account transaction history page
    """
    template_name = 'frontend/account/partials/transactions.html'


class FrontendSettingsDepositsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Account deposits page
    """
    template_name = 'frontend/account/partials/deposits.html'


class FrontendSettingsWithdrawTemplateView(LoginRequiredMixin, TemplateView):
    """
    Account Withdrawals page.
    """
    template_name = 'frontend/account/partials/withdraw.html'


class FrontendResultsTemplateView(LoginRequiredMixin, TemplateView):
    """
    Contest results page
    """
    template_name = 'frontend/results.html'

    def get_context_data(self, **kwargs):
        context = super(FrontendResultsTemplateView, self).get_context_data(**kwargs)

        log_level = self.request.GET.get('loglevel', None)
        if log_level in ['trace', 'debug', 'info', 'warn', 'error']:
            context['loglevel'] = log_level

        if self.request.GET.get('wipe_localstorage', 0) is '1':
            context['wipe_localstorage'] = 1

        return context


class FrontendDraftTemplateView(LoginRequiredMixin, TemplateView):
    """
    Draft a team page.
    """
    # TODO: Check if the draft_group_id GET param is for a valid draft group. 404 otherwise.
    template_name = 'frontend/draft.html'

    def get(self, request, *args, **kwargs):
        draft_group_id = kwargs.get('draft_group_id', 0)
        if UpcomingContestPool.objects.filter(draft_group__pk=int(draft_group_id)).count() == 0:
            return HttpResponseRedirect(reverse('frontend:lobby'))

        return super(FrontendDraftTemplateView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(FrontendDraftTemplateView, self).get_context_data(**kwargs)
        return context


class FrontendPaneTemplateView(TemplateView):
    """
    Right side pane styling and display
    """

    template_name = 'frontend/partials/pane.html'
