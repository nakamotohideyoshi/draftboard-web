#
# settings.py for 'draftboard-dev' heroku app

from dj_database_url import config as heroku_db_config
import urllib

from .base import *

# Constant for determining environment
DOMAIN = 'draftboard-dev.herokuapp.com'
ALLOWED_HOSTS = ['.draftboard-dev.herokuapp.com', '*.draftboard-dev.herokuapp.com', ]

# Connect Heroku database
# Based on https://devcenter.heroku.com/articles/python-concurrency-and-database-connections#number-of-active-connections
# and Django 1.6 we can set 10 persistent connections bc we have a limit of 400 connections with our Premium 2 database.
# 4 workers * up to 10 dynos * 10 connections = 400
# TODO django16 upgrade to persistent connections
DATABASES = {
    'default': heroku_db_config()
}
DATABASES['default']['autocommit'] = True
DATABASES['default']['CONN_MAX_AGE'] = 60

# heroku redis - for api views/pages
HEROKU_REDIS_URL = environ.get('REDIS_URL')
heroku_redis_url = urllib.parse.urlparse(HEROKU_REDIS_URL)
# since we should have a heroku redis instance for production, override the default api cache name
API_CACHE_NAME = 'api'

# Redis caching
redis_url = urllib.parse.urlparse(environ.get('REDISCLOUD_URL'))

CACHES = {
    #
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {"max_connections": 10}
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },

    # separate one to invalidate all of cachalot if need be
    "cachalot": {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },

    # api view cache
    API_CACHE_NAME: {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': "redis://:%s@%s:%s/0" % (heroku_redis_url.password,
                                             heroku_redis_url.hostname,
                                             heroku_redis_url.port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
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
PUSHER_APP_ID = '159461'
PUSHER_KEY = '49224807c21863bf259b'
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_ENABLED = 't' in environ.get('PUSHER_ENABLED', 'true') # heroku config vars are strings!

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_REST_API_BASE = environ.get('PAYPAL_REST_API_BASE')
PAYPAL_CLIENT_ID    = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET       = environ.get('PAYPAL_SECRET')

#
###########################################################################
# Sandbox Account:  paypal-facilitator@draftboard.com
# Access Token:     (from environment var)
##########################################################################
VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

#
# dataden mongo database connection
MONGO_SERVER_ADDRESS    = environ.get('MONGO_SERVER_ADDRESS')   # ie: '123.132.123.123'
MONGO_AUTH_DB           = environ.get('MONGO_AUTH_DB')          # 'admin'
MONGO_USER              = environ.get('MONGO_USER')             # 'admin'
MONGO_PASSWORD          = environ.get('MONGO_PASSWORD')         # 'dataden1'
MONGO_PORT              = int(environ.get('MONGO_PORT'))         # 27017     cast MONGO_PORT to integer!
MONGO_HOST = environ.get('MONGO_HOST') % ( MONGO_USER,
                                            MONGO_PASSWORD,
                                            MONGO_SERVER_ADDRESS,
                                            MONGO_PORT,
                                            MONGO_AUTH_DB )

DATETIME_DELTA_ENABLE = True   # dont do this once production environemnt is actual live!

#
##########################################################################
# trulioo creds
##########################################################################
TRULIOO_API_BASE_URL    = environ.get('TRULIOO_API_BASE_URL')
TRULIOO_USER            = environ.get('TRULIOO_USER')
TRULIOO_PASSWORD        = environ.get('TRULIOO_PASSWORD')