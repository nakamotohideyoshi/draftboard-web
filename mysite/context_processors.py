from django.conf import settings
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