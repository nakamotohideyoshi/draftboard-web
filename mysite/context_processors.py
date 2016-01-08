from django.conf import settings
from util.timeshift import delta_now
from django.utils.dateformat import format

# return the number of reviewable withdraw object

# creates context where the models lowercase name
# indexes to the number of pending ones there are
# the return dict is osmething like:
#
#       {'withdraw_model_badges': {'paypalwithdraw': 4, 'checkwithdraw': 4}}
#
def pusher_key(request):
    return {'PUSHER_KEY': settings.PUSHER_KEY}


# creates context where the models lowercase name
# indexes to the number of pending ones there are
# the return dict is osmething like:
#
#       {'withdraw_model_badges': {'paypalwithdraw': 4, 'checkwithdraw': 4}}
#
def pusher_channel_prefix(request):
    return {'PUSHER_CHANNEL_PREFIX': settings.PUSHER_CHANNEL_PREFIX}


# allows delta_now() method to be in the template
# this way we can pass through the replayer time for testing purposes into javascript
def delta_now_prefix(request):
    return {'DELTA_NOW': format(delta_now(), 'c') }