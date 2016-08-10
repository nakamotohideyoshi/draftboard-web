#
# local.py - settings

from .base import *
from subprocess import check_output
import urllib

DOMAIN = 'localhost'

def get_db_name():
    # Determine db name according to git branch
    git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
    db_name = 'dfs_' + check_output(git_branch_cmd.split()).decode('utf-8')[:-1]
    return db_name

db_name = get_db_name()

DEBUG = True

#
# overrides timezone.now() so that
DATETIME_DELTA_ENABLE = True

#
INSTALLED_APPS = ('test_without_migrations',) + INSTALLED_APPS

#
# This will dump the raw postgres db:
# $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        # 'USER': 'vagrant',  # by not specifying a user at all, it will not prompt for password
        # 'HOST': 'localhost',  # default to localhost
        # 'CONN_MAX_AGE': 60,
    }
}

# local dev redis settings
LOCAL_REDIS_URL = 'redis://127.0.0.1:6379'

# heroku redis - for api views/pages
HEROKU_REDIS_URL = environ.get('REDIS_URL')
heroku_redis_url = urllib.parse.urlparse(HEROKU_REDIS_URL)

# RedisCloud redis - used primarily for live stats
REDISCLOUD_URL = environ.get('REDISCLOUD_URL')
redis_url = urllib.parse.urlparse(REDISCLOUD_URL)

if REDISCLOUD_URL is None:
    REDIS_CACHE_LOCATION = LOCAL_REDIS_URL
else:
    REDIS_CACHE_LOCATION = "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port)

# Run the command `redis-server` in another window to start up caching.
CACHES = {
    # "default": {
    #     "BACKEND": "django_redis.cache.RedisCache",
    #     "LOCATION": REDIS_CACHE_LOCATION,
    #     "OPTIONS": {
    #         "CLIENT_CLASS": "django_redis.client.DefaultClient",
    #         'MAX_ENTRIES': 1000000,
    #     },
    #     # expire caching at max, 1 month
    #     'TIMEOUT': 2592000
    # },

    #
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {"max_connections": 5}
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
        },
    },

    # separate for template caching so we can clear when we want
    "django_templates": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Asset locations
STATIC_URL = '/static/'

# this happens to be the live ec2 mongo
# (Dev) Mongo Connection settings
MONGO_SERVER_ADDRESS = 'ds015781-a0.mlab.com'
MONGO_AUTH_DB = 'admin'
MONGO_USER = 'admin'
MONGO_PASSWORD = 'dataden1'
MONGO_PORT = 15781         # default port may be the actual port
MONGO_HOST = 'mongodb://%s:%s@%s:%s/%s' % (
    MONGO_USER,
    MONGO_PASSWORD,
    MONGO_SERVER_ADDRESS,
    MONGO_PORT,
    MONGO_AUTH_DB)

DATADEN_ASYNC_UPDATES = True  # for dev, we wont always have celery running

#
##########################################################################
#        pusher - DEVELOPMENT ids
##########################################################################
PUSHER_APP_ID = '179543'                            # pbp-stats-linking-dev
PUSHER_KEY = '5a4601521c1e2a3778aa'
PUSHER_SECRET = '2c286ac8c239f8e73f00'
PUSHER_CHANNEL_PREFIX = ''
PUSHER_ENABLED = True

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_REST_API_BASE = 'https://api.sandbox.paypal.com' # 'https://api.paypal.com'
PAYPAL_CLIENT_ID = 'ARqP3lkXhhR_jmm6NkyoKQfuOcBsn1KBYtlzZGHEvGDCQ-ajNoxpQD2mDScpT6tkgsI7qFgVJ-KgzpFE'
PAYPAL_SECRET = 'EOKSd-HCNfWE17mu8e7uyjs2egSla2yXs7joweXCLdimCY8yv-FcCx7LeP1do0gMb9vExJSmjyw9hwRu'

#
###########################################################################
# Sandbox Account:  paypal-facilitator@draftboard.com
# Access Token:     access_token$sandbox$c6yfbzrdmyjqbf6k$4218ebe110f341437affed2f726cd6fa
# Expiry Date:      01 Aug 2026
##########################################################################
VZERO_ACCESS_TOKEN = 'access_token$sandbox$c6yfbzrdmyjqbf6k$4218ebe110f341437affed2f726cd6fa'
#VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

#
# because of the local setup, custom test runner requires root priviledges
# from test.runners import InlineAppDiscoverRunner
# TEST_RUNNER = 'test.runners.InlineAppDiscoverRunner'
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
