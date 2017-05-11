from .production import *

# custom production.py settings file to specifically use the mongolab m3 instance

# Override our default redis max connection limit. At 5 we get
# `UpdateWorker couldnt get redis connection` errors.
#
# If this is too low, you'll get a lot of `Redis ConnectionError: Too many connections` and
# the trigger will start eating tons of memory.
# That error doesn't make much sense but whatever.
overrides = {'CONNECTION_POOL_KWARGS': {'max_connections': 80}}
CACHES['default']['OPTIONS'].update(overrides)
