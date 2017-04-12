from .production import *

# custom production.py settings file to specifically use the mongolab m3 instance

# mongo database connection settings

# environ.get('MONGO_SERVER_ADDRESS')
MONGO_SERVER_ADDRESS = 'ds015781-a0.mlab.com'
# environ.get('MONGO_AUTH_DB')
MONGO_AUTH_DB = 'admin'
# environ.get('MONGO_USER')
MONGO_USER = 'admin'
# environ.get('MONGO_PASSWORD')
MONGO_PASSWORD = 'dataden1'
# int(environ.get('MONGO_PORT')) cast MONGO_PORT to integer!
MONGO_PORT = int(15781)
MONGO_HOST = 'mongodb://%s:%s@%s:%s/%s' % (
    MONGO_USER, MONGO_PASSWORD, MONGO_SERVER_ADDRESS, MONGO_PORT, MONGO_AUTH_DB)

# Override our default redis max connection limit. At 5 we get
# `UpdateWorker couldnt get redis connection` errors.
#
# If this is too low, you'll get a lot of `Redis ConnectionError: Too many connections` and
# the trigger will start eating tons of memory.
# That errordoesn't make much sense but whatever.
overrides = {'CONNECTION_POOL_KWARGS': {'max_connections': 40}}
CACHES['default']['OPTIONS'].update(overrides)
