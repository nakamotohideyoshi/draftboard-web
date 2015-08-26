from django.apps import AppConfig

class ReplayerConfig(AppConfig):
    """
    registers signals
    """

    name = 'replayer'
    verbose_name = 'Replayer'

    def ready(self):
        super().ready()

        import replayer.signals

