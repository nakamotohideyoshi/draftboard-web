# settings.py for 'draftboard-dev' heroku app
from .base import *
from dj_database_url import config as heroku_db_config
from urllib import parse

# Constant for determining environment
DOMAIN = 'dev.draftboard.com'
ALLOWED_HOSTS = [DOMAIN]

# Testing mode off
DEBUG = False

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

# SSL - we redirect all traffic to HTTPS at domain level, no need at application level
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600

# heroku redis - for api views/pages
HEROKU_REDIS_URL = environ.get('REDIS_URL')
heroku_REDIS_URL = parse.urlparse(HEROKU_REDIS_URL)
# since we should have a heroku redis instance for production, override the default api cache name
API_CACHE_NAME = 'api'

# Redis caching
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
            'CONNECTION_POOL_KWARGS': {'max_connections': 10}
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

INSTALLED_APPS += (
    'gunicorn',  # gunicorn for Heroku
    'raven.contrib.django.raven_compat',  # sentry for heroku
)

# Pusher
PUSHER_APP_ID = environ.get('PUSHER_APP_ID')
PUSHER_KEY = environ.get('PUSHER_KEY')
PUSHER_SECRET = environ.get('PUSHER_SECRET')

# Paypal
PAYPAL_REST_API_BASE = environ.get('PAYPAL_REST_API_BASE')
PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = environ.get('PAYPAL_SECRET')
VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

# dataden mongo database connection
# MONGO_SERVER_ADDRESS = environ.get('MONGO_SERVER_ADDRESS')   # ie: '123.132.123.123'
# MONGO_AUTH_DB = environ.get('MONGO_AUTH_DB')          # 'admin'
# MONGO_USER = environ.get('MONGO_USER')             # 'admin'
# MONGO_PASSWORD = environ.get('MONGO_PASSWORD')         # 'dataden1'
# MONGO_PORT = int(environ.get('MONGO_PORT'))         # 27017     cast MONGO_PORT to integer!
# MONGO_HOST = environ.get('MONGO_HOST') % (MONGO_USER,
#                                           MONGO_PASSWORD,
#                                           MONGO_SERVER_ADDRESS,
#                                           MONGO_PORT,
#                                           MONGO_AUTH_DB)

MIDDLEWARE_CLASSES += (
    'account.middleware.access_subdomains.AccessSubdomainsMiddleware',
)
