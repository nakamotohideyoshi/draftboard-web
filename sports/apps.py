from django.apps import AppConfig

class SportsConfig(AppConfig):
    """
    registers signals
    """

    name = 'sports'
    verbose_name = 'Sports'

    def ready(self):
        super().ready()

        import sports.signals


