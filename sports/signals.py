#
# sports/signals.py

from django.dispatch import receiver
from dataden.signals import Ping

# @receiver(signal=Ping.signal)
# def ping_receiver(sender, **kwargs):
#     print(str(sender), 'ping')

class DataDenReceiver(object):
    """
    receiver methods of this class should not get the 'self' argument.
    giving methods 'self' will break the signal mechanism!
    """

    @receiver(signal=Ping.signal)
    def ping(sender, **kwargs):
        """
        dataden's mongodb is sending triggers. this does not indicate
        specifically that dataden is actively parsing. it does mean
        that we are listening to all the transactions which are
        being processed by mongo for any namespaces we have configured.
        """
        print(str(sender), 'ping')
