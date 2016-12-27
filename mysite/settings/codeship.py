import logging

from .local import *

# Disable any logging less than WARNING.
logging.disable(logging.INFO)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': environ.get('PG_USER'),
        'PASSWORD': environ.get('PG_PASSWORD'),
        'HOST': '127.0.0.1',

        # https://codeship.com/documentation/databases/postgresql/
        'PORT': 5434,  # currently using 5434 uses postgres 9.4
    }
}

# Use codeship's redis location in place of redis cloud.
REDIS_URL = 'redis://127.0.0.1:6379/0'
REDIS_URL_CELERY = 'redis://127.0.0.1:6379/1'

# Run the command `redis-server` in another window to start up caching.
# Notice that none of these entries have passwords, because the local docker
# instance does not have one.
CACHES = {
    # default django cache
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 5}
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },
    # separate for template caching so we can clear when we want
    'django_templates': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    # api view cache
    API_CACHE_NAME: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
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

# Have celery run in a sort of "async" mode.
# http://docs.celeryproject.org/projects/django-celery/en/2.4/cookbook/unit-testing.html
CELERY_ALWAYS_EAGER = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
