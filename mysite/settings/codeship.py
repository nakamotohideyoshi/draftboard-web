from os import environ
from .local import *
from urllib import parse

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': environ.get('PG_USER'),
        'PASSWORD': environ.get('PG_PASSWORD'),
        'HOST': '127.0.0.1',

        # https://codeship.com/documentation/databases/postgresql/
        'PORT': 5434,    # currently using 5434 uses postgres 9.4
    }
}

# Use codeship's redis location in place of redis cloud.
REDISCLOUD_URL = 'redis://127.0.0.1:6379'
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

#
# we dont want to run ./manage.py test because
# we've found that some of the INSTALLED_APPS
# have asynchronous effects on other tests
# which is highly undesireable.
#
# this is a list of the order of apps
# from INSTALLED_APPS to run in
# a sandboxed manner per-app.
TEST_SANDBOXED_INSTALLED_APPS = [
    #
    # note - if the app is found in here, it must also
    #        exist in INSTALLED_APPS for it to be run!
    'account',
    'scoring',
]

#
# codeship test environment does not need sudo privledges,
# and since this .py file import local, we need to override it back to False
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = False

#
# dont actually send objects out with codeship!
PUSHER_ENABLED = False
