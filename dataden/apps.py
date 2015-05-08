from django.apps import AppConfig

class DataDenConfig(AppConfig):
    """
    primarily responsible for registering our signals
    """

    name            = 'dataden'
    verbose_name    = 'DataDen'

    def ready(self):
        super().ready()

        import dataden.signals

