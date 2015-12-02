#
# NOTE ABOUT HOW CELERY WORKS AND ITS REQUIREMENTS
#   1.  You need a worker running. ex: $> ./manage.py celery worker --loglevel=info
#   2.  You can now use celery beat. ex: $> ./manage.py celery beat
#   3.  View the logs in the root directory /logs/celeryd.log
#
#   *4. If you want to be able to add periodic tasks using the django admin, run:
#
#       $> celery -A mysite beat -S djcelery.schedulers.DatabaseScheduler
#
#       then visit: http://localhost/admin/djcelery/periodictask/
#
# Of course, this is only an example of how to run celery concurrently in your terminals...

from __future__ import absolute_import

import os

from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import time

#
# setdefault ONLY sets the default value if the key (ie: DJANGO_SETTINGS_MODULE)
# does not already exist. for dev machines, you should set it to
# mysite.settings.local in /etc/profile on linux (see comments in
# manage.py for more explanation)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings.production')

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
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
    # BROKER_URL = 'redis://localhost:6379/0',
    CELERY_RESULT_BACKEND = settings.CACHES['default']['LOCATION'],
    BROKER_URL = settings.CACHES['default']['LOCATION'],

    #: Only add pickle to this list if your broker is secured
    #: from unwanted access (see userguide/security.html)
    CELERY_ACCEPT_CONTENT = ['pickle'],     #['json'],
    CELERY_TASK_SERIALIZER = 'pickle',      #'json',
    CELERY_RESULT_SERIALIZER = 'pickle',    #'json',

    #CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler',

    CELERYBEAT_SCHEDULE = {
        #
        # very fast, low cpu-intensity task. use default queue (ie: dont specify one)
        #
        # this is a task that simply prints 'heartbeat' in the logs.
        # its only real purposes right now is to put
        # tasks in the default queue for testing purposes
        'heartbeat': {
            'task': 'mysite.celery_app.heartbeat',
            'schedule': timedelta(seconds=60),
            # 'args': (16, 16)
            # if no queue is specified uses the default 'celery' queue
        },

        # #
        # ########################################################################
        # # THIS LONG-RUNNING, CRITICAL TASK REQUIRES ITS OWN QUEUE & WORKER     #
        # ########################################################################
        # # this is the tasks that maintains a running dataden process.
        # # without this task, live stats will never be parsed into
        # # the mongolab database.
        # 'dataden': {
        #     'task': 'dataden.tasks.dataden',
        #     'schedule': timedelta(seconds=20),
        #     #
        #     # for this task, the queue in the comment match the queue for
        #     # the corresponding worker in the Procfile
        #     #'options': {'queue' : 'q_dataden'}
        # },

        #
        ########################################################################
        # THIS LONG-RUNNING, CRITICAL TASK REQUIRES ITS OWN QUEUE & WORKER     #
        ########################################################################
        # this is the process monitoring the mongolab instance
        # for any changes, and it sends django signals
        # when it finds new sports data.
        #
        # without this task, stats will never be pushed
        # from the mongo instance to the django/postgres site!
        #
        # see: dataden.watcher.Trigger
        'dataden_trigger': {
            'task': 'dataden.tasks.dataden_trigger',
            'schedule': timedelta(seconds=19),

            #
            # for this task, the queue in the comment match the queue for
            # the corresponding worker in the Procfile
            #'options': {'queue' : 'q_dataden_trigger'}
        },

        'nba_injuries' : {
            'task': 'sports.nba.tasks.update_injuries',
            'schedule': timedelta(minutes=4*60),
        },

        'nhl_injuries' : {
            'task': 'sports.nhl.tasks.update_injuries',
            'schedule': timedelta(minutes=4*60),
        },

        'nfl_injuries' : {
            'task': 'sports.nfl.tasks.update_injuries',
            'schedule': timedelta(minutes=4*60),
        },

        'mlb_injuries' : {
            'task': 'sports.mlb.tasks.update_injuries',
            'schedule': timedelta(minutes=4*60),
        },

        #
        # The ScheduleManager that creates Contests from
        # admin-defined templates on a preset schedule.
        'schedule_contests_for_tomorrow' : {
            'task'      : 'contest.schedule.tasks.create_scheduled_contests',
            #
            # this crontab is overkill, but it is an example
            # of how we can run the ScheduleManager task many
            # times on the same day.

            #
            # run every 30 minutes, but only from 12 to 1, and between 5pm and 11pm
            'schedule'  : crontab(minute='*/30', hour='12,17-23'),
            'args'      : (1,),    # the first integer value is the offset in days for teh scheduler
        },

    },

    CELERY_ENABLE_UTC = True,
    CELERY_TIMEZONE = 'UTC',
    CELERY_TRACK_STARTED = True,

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

@app.task(bind=True, time_limit=2)
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

@app.task(bind=True, time_limit=300)
def payout(self, instance, **kwargs):
    r_payout    = instance.payout()

@app.task(bind=True, time_limit=60) # 60 seconds is an eternity for a stat update
def stat_update(self, updateable, **kwargs):
    #
    # call send() on a dataden.signals.Updateable instance
    updateable.send()

