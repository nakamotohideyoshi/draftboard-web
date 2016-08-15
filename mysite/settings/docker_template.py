from sys import argv
from .local import *

"""
Used to run docker + webpack in a local dev environment

If you have any user-specific settings that are only to be used on your
machine, you should copy this file into YOUR_NAME.py (or whatever) and add
it to the .gitignore file.

You should also set an environment variable to auto-load this file for you:

export DJANGO_SETTINGS_MODULE=mysite.settings.YOUR_NAME
"""

# docker redis locations
REDISCLOUD_URL = 'redis://redis:6379'

# update CACHES from local settings
CACHES['default']['LOCATION'] = REDISCLOUD_URL
CACHES['cachalot']['LOCATION'] = REDISCLOUD_URL
CACHES['django_templates']['LOCATION'] = REDISCLOUD_URL

# served static assets from webpack's devserver
STATIC_URL = 'http://localhost:8090/static/'

# custom prefix for pusher messages
PUSHER_CHANNEL_PREFIX = 'YOURNAMEHERE_'

# use test API
API_TEST_MODE = True

# because celery can runaway over time
if '/usr/bin/celery' in argv:
    DEBUG = False
