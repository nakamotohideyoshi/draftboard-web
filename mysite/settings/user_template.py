from .local import *


"""
    If you have any user-specific settings that are only to be used on your
    machine, you should copy this file into YOUR_NAME.py (or whatever) and add
    it to the .gitignore file.

    You can also set an environment variable to auto-load this file for you:

    export DJANGO_SETTINGS_MODULE=mysite.settings.YOUR_NAME
"""


# Should static files be served from webpack's devserver? If so, this is the
# host of the machine running the devserver.
STATIC_URL = 'http://zachbookpro.local:8080/static/'

# This should be the name of your settings file and a _ after
PUSHER_CHANNEL_PREFIX = 'user_template_'