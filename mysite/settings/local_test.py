from .local import *
import logging

# Disable any logging less than WARNING.
# logging.disable(logging.DEBUG)
LOGGING['loggers'].update({
    'django': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
})


print('Using `local_test.py` settings file.')

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

# Do not send pusher events when testing.
PUSHER_ENABLED = False

# In case we do send pusher events when testing, change the pusher channel so we don't
# interfere with any legit events.
PUSHER_CHANNEL_PREFIX = 'local_test_'

# Have celery run in a sort of "async" mode.
# http://docs.celeryproject.org/projects/django-celery/en/2.4/cookbook/unit-testing.html
CELERY_ALWAYS_EAGER = True
CELERY_TASK_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True
