#
# dataden/signals.py
#
# docs: https://docs.djangoproject.com/en/1.8/topics/signals/

from django.dispatch import Signal

class Ping(object):

    signal = Signal(providing_args=[])

    def send(self):
        self.signal.send_robust(sender=self.__class__)

class Update(object):
    pass

class Push(object):
    pass

class Pull(object):
    pass





