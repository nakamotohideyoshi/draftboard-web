from .local import *

# This has issues with atomic transactions, maybe we can sort it out at some point.

# Default to a tmp sqlite3 db in memory#
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": 'sqlite_testing',
#     },
# }


# This is faster than the default django one
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)


# docker redis locations
# REDIS_CELERY_LOCATION = 'redis://redis:6379/0'
# REDIS_CACHE_LOCATION = 'redis://redis:6379/1'


# update CACHES from local settings
# CACHES['default']['LOCATION'] = REDIS_CACHE_LOCATION
# CACHES['celery']['LOCATION'] = REDIS_CELERY_LOCATION
# CACHES['django_templates']['LOCATION'] = REDIS_CACHE_LOCATION


# This should be the name of your settings file and a _ after
PUSHER_CHANNEL_PREFIX = 'local_test_'
