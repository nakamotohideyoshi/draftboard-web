from django.views.generic.base import TemplateView


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
