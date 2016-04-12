#
# settings.py for 'draftboard-dev' heroku app

from dj_database_url import config as heroku_db_config
from urllib.parse import urlparse

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

# Redis caching
redis_url = urlparse(environ.get('REDISCLOUD_URL'))

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
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
}

# Static assets, served via django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/'

# Testing mode off for production
DEBUG = False
# Match template debugging to what environment debug is
TEMPLATE_DEBUG = DEBUG

# Cache templates
TEMPLATE_LOADERS = (
    ('django.template.loaders.cached.Loader', (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

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
# dataden mongo database connection
MONGO_SERVER_ADDRESS    = environ.get('MONGO_SERVER_ADDRESS')   # ie: '123.132.123.123'
MONGO_AUTH_DB           = environ.get('MONGO_AUTH_DB')          # 'admin'
MONGO_USER              = environ.get('MONGO_USER')             # 'admin'
MONGO_PASSWORD          = environ.get('MONGO_PASSWORD')         # 'dataden1'
MONGO_PORT              = environ.get('MONGO_PORT')             # 27017
MONGO_HOST = environ.get('MONGO_HOST') % ( MONGO_USER,
                                            MONGO_PASSWORD,
                                            MONGO_SERVER_ADDRESS,
                                            MONGO_PORT,
                                            MONGO_AUTH_DB )

DATETIME_DELTA_ENABLE = True   # dont do this once production environemnt is actual live!
