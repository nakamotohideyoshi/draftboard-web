from __future__ import absolute_import
# this will make sure the app is alwasy imported when
# Django starts so that shared task will use this app
from .celery_app import app as celery_app


#
# enable MySiteConfig -- sets up mysite signals (if there are any)
#                     -- sets up timeshift (if enabled on host)
default_app_config = 'mysite.apps.MySiteConfig'

