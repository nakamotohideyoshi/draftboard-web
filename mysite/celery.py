#
# NOTE ABOUT HOW CELERY WORKS AND ITS REQUIREMENTS
#   1.  You need a worker running. ex: $> ./manage.py celery worker --loglevel=info
#   2.  You can now use celery beat. ex: $> ./manage.py celery beat
#   3.  View the logs in the root directory /logs/celeryd.log
#
# Of course, this is only an example of how to run celery concurrently in your terminals...

from __future__ import absolute_import

import os

from celery import Celery
from datetime import timedelta
import time

from pp.classes import Payout

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

from django.conf import settings

app = Celery('mysite')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(settings.INSTALLED_APPS)

# # hook up the database backend
# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
# )

#
# put the settings here, otherwise they could be in
# the main settings.py file, but this is cleaner
app.conf.update(
    #CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    #CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
    BROKER_URL = 'redis://localhost:6379/0',

    #: Only add pickle to this list if your broker is secured
    #: from unwanted access (see userguide/security.html)
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_RESULT_SERIALIZER = 'json',

    #CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler',

    CELERYBEAT_SCHEDULE = {
        # 'heartbeat': {
        #     'task': 'heartbeat',
        #     'schedule': timedelta(seconds=9),
        #     #'args': (16, 16)
        # },

        #
        # this is an example of how to call a function in this .py file
        'heartbeat': {
            'task': 'mysite.celery.heartbeat',
            'schedule': timedelta(seconds=3),
            #'args': (16, 16)
        }
    },

    CELERY_TIMEZONE = 'UTC',

)


#
# BROKER_URL = 'amqp://guest:guest@localhost//'
#
# #: Only add pickle to this list if your broker is secured
# #: from unwanted access (see userguide/security.html)
# CELERY_ACCEPT_CONTENT = ['json']

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def pause(self, t=5.0, msg='finished'):
    time.sleep( t )
    print( msg )
    return True

@app.task(bind=True)
def pause_then_raise(self, t=5.0, msg='finished'):
    time.sleep( t )
    raise Exception('this was throw on purpose to test')
    return True

@app.task(bind=True)
def heartbeat(self):
    print( 'heartbeat' )


class PayoutTask( object ):
    """
    lets extend the Payout object i wrote, and make one of its test functions a test
    """

    @app.task(bind=True)
    def payout(self):
        raise Exception('unimplemented currently')

    @app.task(bind=True)
    def payout_debug(self):
        p = Payout()
        p.payout_debug_test_error_50_percent()