from __future__ import absolute_import

# this will make sure the app is alwasy imported when
# Django starts so that shared task will use this app
from .celery import app as celery_app