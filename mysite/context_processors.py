from django.conf import settings
from django.core.cache import cache
from util.timeshift import get_delta


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
    if settings.DEBUG is True:
        return {'DELTA_NOW': get_delta()}
    else:
        return {'DELTA_NOW': 0}


# allows delta_now() method to be in the template
# this way we can pass through the replayer time for testing purposes into javascript
def player_images_url(request):
    return {'PLAYER_IMAGES_URL': settings.PLAYER_IMAGES_URL}


# returns an md5 hash of the latest git commit uuid
def git_commit_uuid(request):
    return {'GIT_COMMIT_UUID': settings.GIT_COMMIT_UUID}


# returns level of the client logging
def js_loglevel(request):
    return {'JS_LOGLEVEL': cache.get('js_loglevel', '')}
