from subprocess import check_output
from .base import *

def get_db_name():

    # Determine db name according to git branch
    git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
    db_name = 'dfs_' + check_output(git_branch_cmd.split()).decode('utf-8')[:-1]
    return db_name

db_name = get_db_name()

DEBUG = True

#
# try to create the database, if it already exists, this will have no effect
# create_db_cmd = 'sudo -u postgres createdb %s' % db_name
# try:
#     if check_output(create_db_cmd.split()).decode('utf-8').strip() == '':
#         print( 'mysite/settings/local.py >>> created', db_name )
# except Exception:
#     #print( 'could not create', db_name, ' - it may already exist' )
#     pass

#
# Now you can:
#       migrate - you will need to specify the settings file,
#       $> ./manage.py migrate --settings mysite.settings.local
# Or:
#       Ask for a db dump from another dev to then import into the db

#
# This will dump the raw postgres db:
# $> sudo -u postgres pg_dump -Fc --no-acl --no-owner dfs_master > dfs_exported.dump
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        #'USER': 'vagrant',      # by not specifying a user at all, it will not prompt for password
        #'HOST': 'localhost',    # default to localhost
        #'CONN_MAX_AGE': 60,
    }
}

#
# (Dev) Redis Settings
REDIS_FORMAT_URL        = 'redis://%s:%s/%s'
REDIS_HOST              = '127.0.0.1'
REDIS_PORT              = 6379
REDIS_CELERY_DB         = 0
REDIS_CELERY_LOCATION   = REDIS_FORMAT_URL % (REDIS_HOST, REDIS_PORT, REDIS_CELERY_DB)
REDIS_CACHE_DB          = 1
REDIS_CACHE_LOCATION    = REDIS_FORMAT_URL % (REDIS_HOST, REDIS_PORT, REDIS_CACHE_DB)

# Run the command `redis-server` in another window to start up caching.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS"  : "django_redis.client.DefaultClient",
            'MAX_ENTRIES'   : 10000,
        },
        # expire caching at max, 1 month
        'TIMEOUT': 2592000
    },
    # separate one to invalidate all of cachalot if need be
    "cachalot": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_CACHE_LOCATION,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Asset locations
STATIC_URL = '/static/'

# # (Dev) Mongo Connection settings
# MONGO_PASSWORD  = ''
# MONGO_HOST      = 'localhost'
# MONGO_PORT      = 27017         # default port may be the actual port

# dataden mongo database connection
MONGO_AUTH_DB   = 'admin'
MONGO_USER      = 'admin'
MONGO_PASSWORD  = 'dataden1'
MONGO_PORT      = 27017  # NOTE: any port specified in the connection uri string overrides this port
MONGO_HOST      = 'mongodb://%s:%s@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/%s?replicaSet=rs-ds057273' % (MONGO_USER, MONGO_PASSWORD, MONGO_AUTH_DB)
MONGO_CONNECTION_URI = 'mongodb://admin:dataden1@ds057273-a0.mongolab.com:57273,ds057273-a1.mongolab.com:57273/admin?replicaSet=rs-ds057273'

# DATADEN_ASYNC_UPDATES   = False  # for dev, we wont always have celery running

#
##########################################################################
#        pusher - DEVELOPMENT ids
##########################################################################
PUSHER_APP_ID   = '144196'
PUSHER_KEY      = 'f23775e0c1d0da57bb4b'
PUSHER_SECRET   = 'fc815c85237d726b9d8e'