from .base import *
from dj_database_url import config as heroku_db_config
from urllib import parse

# Constant for determining environment
DOMAIN = 'www.draftboard.com'
ALLOWED_HOSTS = [DOMAIN, 'draftboard-prod.herokuapp.com']

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
# TODO django16 upgrade to persistent connections
DATABASES = {
    'default': heroku_db_config()
}
DATABASES['default']['autocommit'] = True
DATABASES['default']['CONN_MAX_AGE'] = 500

# SSL - we redirect all traffic to HTTPS at domain level, no need at application level
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_SECONDS = 31536000  # one year, prevents accepting traffic via HTTP
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # set this if all subdomains are under HTTPS

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
            'CONNECTION_POOL_KWARGS': {'max_connections': 2}
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

# Static assets, served via cloudfront + django-whitenoise
STATIC_URL = environ.get('DJANGO_STATIC_HOST', '') + '/static/'

INSTALLED_APPS += (
    'gunicorn',  # gunicorn for Heroku
)

# Pusher
PUSHER_APP_ID = environ.get('PUSHER_APP_ID')
PUSHER_KEY = environ.get('PUSHER_KEY')
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_CHANNEL_PREFIX = ''  # must remain empty for production!

# Paypal
PAYPAL_REST_API_BASE = environ.get('PAYPAL_REST_API_BASE')
PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = environ.get('PAYPAL_SECRET')
VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

# Don't allow time travel on production!
DATETIME_DELTA_ENABLE = False

# Inactive users
INACTIVE_USERS_EMAILS = [
    'pedro@runitonce.com',
    'dan@runitonce.com',
]

# Trulioo creds
TRULIOO_API_BASE_URL = 'https://api.globaldatacompany.com'
TRULIOO_USER = 'Draftboard_API'
TRULIOO_PASSWORD = 'b8)8=799yf&#jN,'
TRULIOO_DEMO_MODE = False

KISS_ANALYTICS_CODE = '38999ef9bc7158192a6d6dfcc27004c48ed13538'
