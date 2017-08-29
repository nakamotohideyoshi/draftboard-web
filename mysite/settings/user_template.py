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

# when we run the export_pusher_events management command, this will output events to a file
# PUSHER_ENABLED = True
# PUSHER_OUTPUT_TO_FILE = True


# This is for testing gidx webhooks. (`ngrok http 8000` to start)
# If you don't know what this is you can safely ignore it and party on.
# GIDX_WEBHOOK_URL = 'http://a032f89c.ngrok.io'
