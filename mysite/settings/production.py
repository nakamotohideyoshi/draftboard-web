from dj_database_url import config as heroku_db_config
from urllib.parse import urlparse

from .base import *

# Constant for determining environment
DOMAIN = 'rio-dfs.herokuapp.com'

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

# Set django-lockdown to run on heroku for now
USE_LOCKDOWN = os.environ.get('USE_LOCKDOWN', 'False') == 'True'
if USE_LOCKDOWN:
    INSTALLED_APPS += ('lockdown',)
    MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware',)
    LOCKDOWN_PASSWORDS = (os.environ.get('LOCKDOWN_PASSWORD', 'False'),)
    # LOCKDOWN_URL_EXCEPTIONS = (r'^/some/url/not/locked/down/$',)

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
PUSHER_APP_ID = '144195'
PUSHER_KEY = '9754d03a7816e43abb64'
PUSHER_SECRET = environ.get('PUSHER_SECRET')

#
# dataden mongo database connection
MONGO_AUTH_DB   = 'admin'
MONGO_USER      = 'admin'
MONGO_PASSWORD  = 'dataden1'
MONGO_PORT      = 27017  # NOTE: any port specified in the connection uri string overrides this port
MONGO_HOST      = 'mongodb://%s:%s@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/%s?replicaSet=rs-ds057273' % (MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_DB)
# MONGO_CONNECTION_URI = 'mongodb://admin:dataden1@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/admin?replicaSet=rs-ds057273'

# # if this config var exists, override the default production value
# dataden_mongo_uri = urlparse(environ.get('DATADEN_MONGO_URI'))
# if dataden_mongo_uri:
#     MONGO_HOST = dataden_mongo_uri