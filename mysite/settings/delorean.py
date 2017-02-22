#
# settings.py for 'draftboard-dev' heroku app

from dj_database_url import config as heroku_db_config
from urllib import parse

from .base import *

# Constant for determining environment
DOMAIN = 'delorean.draftboard.com'
ALLOWED_HOSTS = [DOMAIN]


# Testing mode off for production
DEBUG = False


# Connect Heroku database
"""
Based on: https://devcenter.heroku.com/articles/python-concurrency-and-database-connections#number-o
f-active-connections

And Django 1.6 we can set 10 persistent connections bc we have a limit of 400 connections with our
Premium 2 database.
4 workers * up to 10 dynos * 10 connections = 400
"""
DATABASES = {
    'default': heroku_db_config()
}
DATABASES['default']['autocommit'] = True
DATABASES['default']['CONN_MAX_AGE'] = 500

DEFAULT_FROM_EMAIL = 'support+staging@draftboard.com'

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600

# since we should have a heroku redis instance for production, override the default api cache name
API_CACHE_NAME = 'api'

# RedisCloud redis - used primarily for live stats
REDIS_URL = environ.get('REDISCLOUD_URL')
REDIS_URL_CELERY = environ.get('REDISCLOUD_URL_CELERY')

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

# Static assets, served via django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/'

# Add gunicorn
INSTALLED_APPS += (
    'gunicorn',
)

# Pusher
PUSHER_APP_ID = environ.get('PUSHER_APP_ID')
PUSHER_KEY = environ.get('PUSHER_KEY')
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_ENABLED = 't' in environ.get('PUSHER_ENABLED', 'true')  # heroku config vars are strings!


##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_REST_API_BASE = environ.get('PAYPAL_REST_API_BASE')
PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = environ.get('PAYPAL_SECRET')

##########################################################################
# paypal vzero minimal deposit server access_token
##########################################################################
VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

# dont allow updates to be saved.
# they are only being sent if they already exist!
DISABLE_REPLAYER_UPDATE_RECORDING = True

# Allow time travel on delorean server!
DATETIME_DELTA_ENABLE = True

# Inactive users
INACTIVE_USERS_EMAILS = []


MIDDLEWARE_CLASSES += (
    'account.middleware.access_subdomains.AccessSubdomainsMiddleware',
)
