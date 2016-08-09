#
# production.py
from .base import *

from dj_database_url import config as heroku_db_config
import urllib

# Constant for determining environment
DOMAIN = 'www.draftboard.com'

ALLOWED_HOSTS = [ DOMAIN, 'draftboard-prod.herokuapp.com']
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

# RedisCloud redis - used primarily for live stats
REDISCLOUD_URL = environ.get('REDISCLOUD_URL')
redis_url = urllib.parse.urlparse(REDISCLOUD_URL)

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

    # separate for template caching so we can clear when we want
    "django_templates": {
        "BACKEND": "django_redis.cache.RedisCache",
        'LOCATION': "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
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

# SSL
# NOTE: we redirect all traffic to HTTPS at the DNS level, no need at application level
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
# SECURE_HSTS_SECONDS = 31536000  # one year, prevents accepting traffic via HTTP

# set this once all subdomains are under HTTPS
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Pusher
PUSHER_APP_ID = '144195'
PUSHER_KEY = '9754d03a7816e43abb64'
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_ENABLED = 't' in environ.get('PUSHER_ENABLED', 'true')  # heroku config vars are strings!

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_REST_API_BASE = environ.get('PAYPAL_REST_API_BASE')
PAYPAL_CLIENT_ID = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET = environ.get('PAYPAL_SECRET')

#
##########################################################################
# paypal vzero minimal deposit server access_token
##########################################################################
VZERO_ACCESS_TOKEN = environ.get('VZERO_ACCESS_TOKEN')

#
# dataden mongo database connection
MONGO_SERVER_ADDRESS = environ.get('MONGO_SERVER_ADDRESS')      # str, ie: '123.132.123.123'
MONGO_AUTH_DB = environ.get('MONGO_AUTH_DB')                    # str
MONGO_USER = environ.get('MONGO_USER')                          # str
MONGO_PASSWORD = environ.get('MONGO_PASSWORD')                  # str
MONGO_PORT = int(environ.get('MONGO_PORT'))                     # str (should be cast to int)
MONGO_HOST = environ.get('MONGO_HOST') % (MONGO_USER,
                                          MONGO_PASSWORD,
                                          MONGO_SERVER_ADDRESS,
                                          MONGO_PORT,
                                          MONGO_AUTH_DB)

#
DATETIME_DELTA_ENABLE = True   # dont do this once production environemnt is actual live!

#
SLACK_UPDATES = False
slack_updates = environ.get('SLACK_UPDATES', None)
if slack_updates is not None and 't' in str(slack_updates).lower():
    SLACK_UPDATES = True

#
##########################################################################
# trulioo creds
##########################################################################
TRULIOO_API_BASE_URL    = environ.get('TRULIOO_API_BASE_URL')
TRULIOO_USER            = environ.get('TRULIOO_USER')
TRULIOO_PASSWORD        = environ.get('TRULIOO_PASSWORD')