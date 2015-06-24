#
# dataden/signals.py
#
# docs: https://docs.djangoproject.com/en/1.8/topics/signals/

from mysite.celery_app import stat_update

from django.dispatch import Signal

class SignalNotSetupProperlyException(Exception):
    def __init__(self, class_name, variable_name):
       super().__init__('You must set "signal"')

class AbstractSignal(object):
    """
    all dataden.signals.py should inherit this object.
    """

    signal = None # child will have to set this

    def __init__(self):
        self.__validate()

    def send(self, **kwargs):
        self.signal.send(sender=self.__class__, **kwargs)

    def __validate(self):
        if self.signal is None:
            raise SignalNotSetupProperlyException(self.__class__.__name__, 'signal')

class Ping(object):

    signal = Signal(providing_args=[])

    def send(self):
        self.signal.send_robust(sender=self.__class__)

class Updateable(object):

    def __init__(self, update):
        self.update = update

    def send(self):
        self.update.send()

class Update(AbstractSignal):
    """
    a signal that contains an object with stats that need to be saved
    """

    signal = Signal(providing_args=['sport','object','parent_api'])

    def __init__(self, o):
        super().__init__()
        self.o = o # a Hashable object created created from oplog entry

    def send(self, async=False):
        """
        call parent send() with the object which has had a change to it
        """
        if async:
            updateable = Updateable( self )
            stat_update.apply_async( (updateable, ), serializer='pickle' )
        else:
            super().send( o=self.o )

class Push(object):
    """
    im playing around with the idea of sending data
    """
    pass

class Pull(object):
    """
    ... but also the idea of telling it about the data it should pull
    """
    pass





