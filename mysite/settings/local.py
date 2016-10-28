from .base import *
from subprocess import check_output
import os
import raven


# Constant for determining environment
DOMAIN = 'localhost'

# Asset locations
STATIC_URL = '/static/'

# overrides timezone.now() so that we can time travel
DATETIME_DELTA_ENABLE = True

# For dev, we wont always have celery running
DATADEN_ASYNC_UPDATES = True

# we dont want to record locally (especially for a machine running a replay!)
DISABLE_REPLAYER_UPDATE_RECORDING = True

# Disable migrations when running your Django tests
INSTALLED_APPS = ('test_without_migrations',) + INSTALLED_APPS

# Determine db name according to git branch
git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
db_name = 'dfs_' + check_output(git_branch_cmd.split()).decode('utf-8')[:-1]

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

# Use the default redis location in base.py
REDIS_CACHE_LOCATION = REDISCLOUD_URL

# Run the command `redis-server` in another window to start up caching.
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },

    # separate one to invalidate all of cachalot if need be
    'cachalot': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },

    # separate for template caching so we can clear when we want
    'django_templates': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_CACHE_LOCATION,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
}

# because of the local setup, custom test runner requires root priviledges
# from test.runners import InlineAppDiscoverRunner
# TEST_RUNNER = 'test.runners.InlineAppDiscoverRunner'
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = True

# Add query counting per request locally
MIDDLEWARE_CLASSES = ('mysite.middleware.query_count_debug.QueryCountDebugMiddleware',) + MIDDLEWARE_CLASSES
LOGGING['loggers'].update({
    'mysite.middleware.query_count_debug.QueryCountDebugMiddleware': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
})

# Sentry
RAVEN_CONFIG = {
    'dsn': 'https://bbae8e8654e34a80b02999b5ade6fd81:77f1b701685044fb9b20d31aa135ce63@sentry.io/72241',
}
