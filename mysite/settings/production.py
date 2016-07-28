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

# Redis caching
redis_url = urllib.parse.urlparse(environ.get('REDISCLOUD_URL'))

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': "redis://:%s@%s:%s/0" % (redis_url.password, redis_url.hostname, redis_url.port),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'CONNECTION_POOL_KWARGS': {"max_connections": 16}
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

# Add gunicorn
INSTALLED_APPS += (
    'gunicorn',

    # sentry for heroku
    'raven.contrib.django.raven_compat',
)

# SSL redirect
MIDDLEWARE_CLASSES += ('mysite.middleware.ssl_redirect.SSLRedirect',)

# Pusher
PUSHER_APP_ID = '144195'
PUSHER_KEY = '9754d03a7816e43abb64'
PUSHER_SECRET = environ.get('PUSHER_SECRET')
PUSHER_ENABLED = 't' in environ.get('PUSHER_ENABLED', 'true') # heroku config vars are strings!

#
##########################################################################
#        paypal client_id, secret keys
##########################################################################
PAYPAL_CLIENT_ID    = environ.get('PAYPAL_CLIENT_ID')
PAYPAL_SECRET       = environ.get('PAYPAL_SECRET')

#
# dataden mongo database connection
MONGO_SERVER_ADDRESS    = environ.get('MONGO_SERVER_ADDRESS')   # ie: '123.132.123.123'
MONGO_AUTH_DB           = environ.get('MONGO_AUTH_DB')          # 'admin'
MONGO_USER              = environ.get('MONGO_USER')             # 'admin'
MONGO_PASSWORD          = environ.get('MONGO_PASSWORD')         # 'dataden1'
MONGO_PORT              = int(environ.get('MONGO_PORT'))        # 27017              cast MONGO_PORT to integer!
MONGO_HOST = environ.get('MONGO_HOST') % ( MONGO_USER,
                                            MONGO_PASSWORD,
                                            MONGO_SERVER_ADDRESS,
                                            MONGO_PORT,
                                            MONGO_AUTH_DB )

# previous MONGO_HOST:
# mongodb://%s:%s@ds057273-a1.mongolab.com:57273,ds057273-a0.mongolab.com:57273/%s?replicaSet=rs-ds057273

#
DATETIME_DELTA_ENABLE = True   # dont do this once production environemnt is actual live!

SLACK_UPDATES = False
slack_updates = environ.get('SLACK_UPDATES', None)
if slack_updates is not None and 't' in str(slack_updates).lower():
    SLACK_UPDATES = True