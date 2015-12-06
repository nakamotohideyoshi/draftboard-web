from django.apps import AppConfig

class ContestConfig(AppConfig):
    """
    primarily responsible for registering our signals
    """

    name            = 'contest'
    verbose_name    = 'Contest'

    def ready(self):
        super().ready()

        import contest.signals