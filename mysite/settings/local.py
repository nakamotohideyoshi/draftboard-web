from subprocess import check_output

from .base import *

# Determine db name according to git branch
git_branch_cmd = 'git rev-parse --abbrev-ref HEAD'
db_name = 'dfs_' + check_output(git_branch_cmd.split())[:-1]

# Run the Postgres OSX app by Heroku.
# Create database by running `psql -d postgres -c "CREATE DATABASE rio_[BRANCH_NAME];"` in terminal
# Ask for a db dump from another dev to then import into the db
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': db_name,
        'USER': 'postgres',
        'HOST': 'localhost',
        'CONN_MAX_AGE': 60,
    }
}

# Redis settings
# Run the command `redis-server` in another window to start up caching.
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
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
