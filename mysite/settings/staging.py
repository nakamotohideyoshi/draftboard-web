# settings.py for 'draftboard-staging' heroku app
from .base import *
from dj_database_url import config as heroku_db_config

# Constant for determining environment
DOMAIN = 'staging.draftboard.com'
ALLOWED_HOSTS = [DOMAIN]

ENVIRONMENT_NAME = "STAGING"
ENVIRONMENT_COLOR = "#9ea548"

# Testing mode off
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

DEFAULT_FROM_EMAIL = 'support+STAGING@draftboard.com'
SITE_ADMIN_EMAIL = ['devs@draftboard.com']
FLAGGED_IDENTITY_EMAIL_RECIPIENTS = []
INACTIVE_USERS_EMAILS = []

# SSL - we redirect all traffic to HTTPS at domain level, no need at application level
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # set this if all subdomains are under HTTPS

# since we should have a heroku redis instance for production, override the default api cache name
API_CACHE_NAME = 'api'

# Redis caching
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

INSTALLED_APPS += (
    'gunicorn',  # gunicorn for Heroku
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

# Don't allow time travel on staging!
DATETIME_DELTA_ENABLE = False

MIDDLEWARE_CLASSES += (
    # Instead of this cookie middleware, we're goign to use lockdown on the
    # staging site since it's easier for non-technical users.
    # 'account.middleware.access_subdomains.AccessSubdomainsMiddleware',
)

# Environment-set gidx credentials
GIDX_API_URL = environ.get('GIDX_API_URL')
GIDX_API_KEY = environ.get('GIDX_API_KEY')
GIDX_MERCHANT_ID = environ.get('GIDX_MERCHANT_ID')
# Gets appended to customer ID's to show they are testing IDs.
GIDX_CUSTOMER_ID_PREFIX = ''
# This is is a prefix to enable testing mode on the client-side of things.
# Set to 'GIDXSB_' to enable. An empty prefix disables testing mode.
GIDX_MERCHANT_SESSION_ID_PREFIX = environ.get('GIDX_MERCHANT_SESSION_ID_PREFIX')
GIDX_PRODUCT_ID = environ.get('GIDX_PRODUCT_ID')
GIDX_ACTIVITY_ID = environ.get('GIDX_ACTIVITY_ID')
GIDX_DEVICE_ID = environ.get('GIDX_DEVICE_ID')

# Should we allow previously claimed ID's to be verified?
# This should ONLY be True for testing.
GIDX_ALLOW_PREVIOUSLY_CLAIMED_ID = True
