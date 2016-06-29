from subprocess import check_output
from .base import *

def get_db_name():

    # Determine db name according to git branch
    git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
    db_name = 'dfs_' + check_output(git_branch_cmd.split()).decode('utf-8')[:-1]
    return db_name

db_name = get_db_name()

DEBUG               = True

#
# overrides timezone.now() so that
DATETIME_DELTA_ENABLE  = True

#
#
INSTALLED_APPS = ('test_without_migrations',) + INSTALLED_APPS
#print(str(INSTALLED_APPS))

#
# try to create the database, if it already exists, this will have no effect
# create_db_cmd = 'sudo -u postgres createdb %s' % db_name
# try:
#     if check_output(create_db_cmd.split()).decode('utf-8').strip() == '':
#         print( 'mysite/settings/local.py >>> created', db_name )
# except Exception:
#     #print( 'could not create', db_name, ' - it may already exist' )
#     pass

#
# Now you can:
#       migrate - you will need to specify the settings file,
#       $> ./manage.py migrate --settings mysite.settings.local
# Or:
#       Ask for a db dump from another dev to then import into the db

#
# This will dump the raw postgres db:
# $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':  db_name,
        #'USER': 'vagrant',      # by not specifying a user at all, it will not prompt for password
        #'HOST': 'localhost',    # default to localhost
        #'CONN_MAX_AGE': 60,
    }
}

#
# (Dev) Redis Settings
REDIS_FORMAT_URL        = 'redis://%s:%s/%s'
REDIS_HOST              = '127.0.0.1'
REDIS_PORT              = 6379
REDIS_CELERY_DB         = 0
REDIS_CELERY_LOCATION   = REDIS_FORMAT_URL % (REDIS_HOST, REDIS_PORT, REDIS_CELERY_DB)
REDIS_CACHE_DB          = 1
REDIS_CACHE_LOCATION    = REDIS_FORMAT_URL % (REDIS_HOST, REDIS_PORT, REDIS_CACHE_DB)

# Run the command `redis-server` in another window to start up caching.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS"  : "django_redis.client.DefaultClient",
            'MAX_ENTRIES'   : 10000,
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },
    # separate one to invalidate all of cachalot if need be
    "cachalot": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#     }
# }

# Asset locations
STATIC_URL = '/static/'

# this happens to be the live ec2 mongo
# (Dev) Mongo Connection settings
MONGO_SERVER_ADDRESS    = 'ds015781-a0.mlab.com'
MONGO_AUTH_DB           = 'admin'
MONGO_USER              = 'admin'
MONGO_PASSWORD          = 'dataden1'
MONGO_PORT              = 15781         # default port may be the actual port
MONGO_HOST = 'mongodb://%s:%s@%s:%s/%s' % (
                    MONGO_USER,
                    MONGO_PASSWORD,
                    MONGO_SERVER_ADDRESS,
                    MONGO_PORT,
                    MONGO_AUTH_DB )

DATADEN_ASYNC_UPDATES   = True  # for dev, we wont always have celery running

#
##########################################################################
#        pusher - DEVELOPMENT ids
##########################################################################
# PUSHER_APP_ID           = '144195'    # production
# PUSHER_KEY              = '9754d03a7816e43abb64'
# PUSHER_SECRET           = 'fcbe16f4bf9e8c0b2b51'
PUSHER_APP_ID           = '179543'    # pbp-stats-linking-dev
PUSHER_KEY              = '5a4601521c1e2a3778aa'
PUSHER_SECRET           = '2c286ac8c239f8e73f00'
PUSHER_CHANNEL_PREFIX   = ''
PUSHER_ENABLED          = True

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_CLIENT_ID    = 'ARqP3lkXhhR_jmm6NkyoKQfuOcBsn1KBYtlzZGHEvGDCQ-ajNoxpQD2mDScpT6tkgsI7qFgVJ-KgzpFE'
PAYPAL_SECRET       = 'EOKSd-HCNfWE17mu8e7uyjs2egSla2yXs7joweXCLdimCY8yv-FcCx7LeP1do0gMb9vExJSmjyw9hwRu'

#
# because of the local setup, custom test runner requires root priviledges
# from test.runners import InlineAppDiscoverRunner
#TEST_RUNNER = 'test.runners.InlineAppDiscoverRunner'
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = True

#
# we dont want to record locally (especially for a machine running a replay!)
DISABLE_REPLAYER_UPDATE_RECORDING = True

#
MIDDLEWARE_CLASSES = ('mysite.middleware.query_count_debug.QueryCountDebugMiddleware',) + MIDDLEWARE_CLASSES

LOGGING['loggers'].update({'mysite.middleware.query_count_debug.QueryCountDebugMiddleware': {
        'handlers': ['console'],
        'level': 'DEBUG',
        }
    })
