from dj_database_url import config as heroku_db_config
from urllib import parse
from .base import *

# Constant for determining environment
DOMAIN = 'draftboard-ios-sandbox.herokuapp.com'
ALLOWED_HOSTS = ['.draftboard-ios-sandbox.herokuapp.com',
                 '*.draftboard-ios-sandbox.herokuapp.com', ]

# Connect Heroku database
# Based on https://devcenter.heroku.com/articles/python-concurrency-and-database-connections#number-of-active-connections
# and Django 1.6 we can set 10 persistent connections bc we have a limit of 400 connections with our Premium 2 database.
# 4 workers * up to 10 dynos * 10 connections = 400
# TODO django16 upgrade to persistent connections
DATABASES = {
    'default': heroku_db_config()
}
DATABASES['default']['autocommit'] = True
DATABASES['default']['CONN_MAX_AGE'] = 500

# RedisCloud redis - used primarily for live stats
REDISCLOUD_URL = environ.get('REDISCLOUD_URL')
REDIS_URL = parse.urlparse(REDISCLOUD_URL)

CACHES = {
    # default django cache
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%s@%s:%s/0' % (
            REDIS_URL.password,
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {'max_connections': 5}
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },
    # Celery cache
    'celery': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%s@%s:%s/1' % (
            REDIS_URL.password,
            REDIS_URL.hostname,
            REDIS_URL.port),
    },
    # separate one to invalidate all of cachalot if need be
    'cachalot': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%s@%s:%s/2' % (
            REDIS_URL.password,
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    # separate for template caching so we can clear when we want
    'django_templates': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%s@%s:%s/3' % (
            REDIS_URL.password,
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    },
    # api view cache
    API_CACHE_NAME: {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://:%s@%s:%s/4' % (
            REDIS_URL.password,
            REDIS_URL.hostname,
            REDIS_URL.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
    }
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

#
# dataden mongo database connection
MONGO_AUTH_DB = 'admin'
MONGO_USER = 'admin'
MONGO_PASSWORD = 'dataden1'
MONGO_PORT = 27017  # NOTE: any port specified in the connection uri string overrides this port
MONGO_HOST = 'mongodb://%s:%s@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/%s?replicaSet=rs-ds057273' % (
    MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_DB)
# MONGO_CONNECTION_URI = 'mongodb://admin:dataden1@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/admin?replicaSet=rs-ds057273'

# # if this config var exists, override the default production value
# dataden_mongo_uri = urlparse(environ.get('DATADEN_MONGO_URI'))
# if dataden_mongo_uri:
#     MONGO_HOST = dataden_mongo_uri

DATETIME_DELTA_ENABLE = True   # dont do this once production environemnt is actual live!
