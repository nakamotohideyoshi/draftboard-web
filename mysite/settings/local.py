from subprocess import check_output
from .base import *

# Determine db name according to git branch
git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
db_name = 'dfs_' + check_output(git_branch_cmd.split()).decode('utf-8')[:-1]

#
# try to create the database, if it already exists, this will have no effect
create_db_cmd = 'sudo -u postgres createdb %s' % db_name
try:
    if check_output(create_db_cmd.split()).decode('utf-8').strip() == '':
        print( 'mysite/settings/local.py >>> created', db_name )
except Exception:
    print( 'could not create', db_name, ' - it may already exist' )

#
# Run the Postgres OSX app by Heroku.

#
# Now you can:
#       migrate - you will need to specify the settings file,
#       $> ./manage.py migrate --settings mysite.settings.local
# Or:
#       Ask for a db dump from another dev to then import into the db

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        #'USER': 'vagrant',      # by not specifying a user at all, it will not prompt for password
        #'HOST': 'localhost',    # default to localhost
        #'CONN_MAX_AGE': 60,
    }
}

# Redis settings
# Run the command `redis-server` in another window to start up caching.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
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
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Asset locations
STATIC_URL = '/static/'

#
# we will need a better way of connecting to mongo for production, but for dev:
from pymongo import MongoClient
def get_mongo_client():
    return MongoClient() # defaults to localhost:27017  or whatever the standard port is