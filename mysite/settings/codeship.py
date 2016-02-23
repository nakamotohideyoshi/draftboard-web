from subprocess import check_output
from .local import *


DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'test',
    'USER': os.environ.get('PG_USER'),
    'PASSWORD': os.environ.get('PG_PASSWORD'),
    'HOST': '127.0.0.1',
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
