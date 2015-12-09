from django.apps import AppConfig

class MySiteConfig(AppConfig):
    """
    primarily responsible for registering our signals,

    AND

    applies timeshift.py
    """

    name            = 'mysite'
    verbose_name    = 'MySite'

    def ready(self):
        super().ready()

        from django.conf import settings
        from django.utils import timezone
        # import os
        # running_on_codeship = os.environ.get('CI', None)
        if settings.DATETIME_DELTA_ENABLE: # and not running_on_codeship:
            import util.timeshift as timeshift
            timezone.now = timeshift.delta_now

