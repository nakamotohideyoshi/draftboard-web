from .base import *
from subprocess import check_output
import os
import raven
from urllib import parse

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

# Use the local Docker redis location in place of redis cloud.
REDISCLOUD_URL = 'redis://redis:6379/'
REDIS_URL = parse.urlparse(REDISCLOUD_URL)

# Run the command `redis-server` in another window to start up caching.
# Notice that none of these entries have passwords, because the local docker
# instance does not have one.
CACHES = {
    # default django cache
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/0' % (
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },
    # Celery cache
    'celery': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/1' % (
            REDIS_URL.hostname,
            REDIS_URL.port),
    },
    # separate one to invalidate all of cachalot if need be
    'cachalot': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/2' % (
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    # separate for template caching so we can clear when we want
    'django_templates': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/3' % (
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    # api view cache
    API_CACHE_NAME: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://%s:%s/4' % (
            REDIS_URL.hostname,
            REDIS_URL.port),
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
MIDDLEWARE_CLASSES = (
    'mysite.middleware.query_count_debug.QueryCountDebugMiddleware',) + MIDDLEWARE_CLASSES
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
MIDDLEWARE_CLASSES += (
    'account.middleware.access_subdomains.AccessSubdomainsMiddleware',
)
