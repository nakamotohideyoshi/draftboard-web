from os import environ
from .local import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'test',
        'USER': environ.get('PG_USER'),
        'PASSWORD': environ.get('PG_PASSWORD'),
        'HOST': '127.0.0.1',

        # https://codeship.com/documentation/databases/postgresql/
        'PORT': 5434,    # currently using 5434 uses postgres 9.4
    }
}

#
# we dont want to run ./manage.py test because
# we've found that some of the INSTALLED_APPS
# have asynchronous effects on other tests
# which is highly undesireable.
#
# this is a list of the order of apps
# from INSTALLED_APPS to run in
# a sandboxed manner per-app.
TEST_SANDBOXED_INSTALLED_APPS = [
    #
    # note - if the app is found in here, it must also
    #        exist in INSTALLED_APPS for it to be run!
    'account',
    'scoring',
]

#
# codeship test environment does not need sudo privledges,
# and since this .py file import local, we need to override it back to False
INLINE_APP_DISCOVER_RUNNER_REQURES_SUDO = False

#
# dont actually send objects out with codeship!
PUSHER_ENABLED = False
