from django.dispatch import Signal
class AbstractSignal(object):
    """
    all signals should inherit this object.
    """

    signal = None # child will have to set this

    def __init__(self):
        self.__validate()

    def send(self, **kwargs):
        self.signal.send(sender=self.__class__, **kwargs)

    def __validate(self):
        if self.signal is None:
            raise SignalNotSetupProperlyException(self.__class__.__name__, 'signal')
