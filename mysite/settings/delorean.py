#
# settings.py for 'draftboard-dev' heroku app

from dj_database_url import config as heroku_db_config
from urllib import parse

from .base import *

# Constant for determining environment
DOMAIN = 'delorean.draftboard.com'
ALLOWED_HOSTS = [DOMAIN]

# Connect Heroku database
# Based on https://devcenter.heroku.com/articles/python-concurrency-and-database-connections#number-of-active-connections
# and Django 1.6 we can set 10 persistent connections bc we have a limit of 400 connections with our Premium 2 database.
# 4 workers * up to 10 dynos * 10 connections = 400
DATABASES = {
    'default': heroku_db_config()
}
DATABASES['default']['autocommit'] = True
DATABASES['default']['CONN_MAX_AGE'] = 500

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

# Testing mode off for production
DEBUG = False

# Add gunicorn
INSTALLED_APPS += (
    'gunicorn',

    # sentry for heroku
    'raven.contrib.django.raven_compat',
)

# Pusher
PUSHER_APP_ID = '159447'
PUSHER_KEY = '32343d7634872062c03e'
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

DATETIME_DELTA_ENABLE = True   # time travel

# dont allow updates to be saved.
# they are only being sent if they already exist!
DISABLE_REPLAYER_UPDATE_RECORDING = True
