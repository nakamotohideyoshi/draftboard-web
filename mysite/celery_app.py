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
import redis
from celery import Celery
from celery.schedules import crontab
import celery.states
from datetime import timedelta
import time
from django.core.cache import cache
from hashlib import md5

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

# i want to know if DEBUG is on or not
print('celery_app settings.DEBUG:', settings.DEBUG)

# # hook up the database backend
# app.conf.update(
#     CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
# )

ALL_SPORTS = ['nba','nhl','mlb','nfl']

#
broker_url = None
redis_url = os.environ.get('REDISCLOUD_URL')
if redis_url is None:
    broker_url = settings.CACHES['default']['LOCATION']
else:
    broker_url = '%s/0' % redis_url

#
# put the settings here, otherwise they could be in
# the main settings.py file, but this is cleaner
app.conf.update(
    #CELERY_RESULT_BACKEND='djcelery.backends.database:DatabaseBackend',
    #CELERY_RESULT_BACKEND='djcelery.backends.cache:CacheBackend',
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0',
    # BROKER_URL = 'redis://localhost:6379/0',
    # CELERY_RESULT_BACKEND = settings.CACHES['default']['LOCATION'],
    # BROKER_URL = settings.CACHES['default']['LOCATION'],
    #CELERY_RESULT_BACKEND = os.environ.get('REDISCLOUD_URL'),
    BROKER_URL = broker_url,

    #: Only add pickle to this list if your broker is secured
    #: from unwanted access (see userguide/security.html)
    CELERY_ACCEPT_CONTENT = ['pickle'],     #['json'],
    CELERY_TASK_SERIALIZER = 'pickle',      #'json',
    CELERY_RESULT_SERIALIZER = 'pickle',    #'json',

    #CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler',

    CELERYBEAT_SCHEDULE = {
        #
        # contest pool schedule manager updates the upcoming
        # days with what is going to be created.
        'nba_contest_pool_schedule_manager' : {
            'task' : 'contest.schedule.tasks.contest_pool_schedule_manager',
            'schedule' : timedelta(hours=4),
            'args'      : ('nba',),
        },
        'nhl_contest_pool_schedule_manager' : {
            'task' : 'contest.schedule.tasks.contest_pool_schedule_manager',
            'schedule' : timedelta(hours=4, minutes=3),  # staggered
            'args'      : ('nhl',),
        },
        'mlb_contest_pool_schedule_manager' : {
            'task' : 'contest.schedule.tasks.contest_pool_schedule_manager',
            'schedule' : timedelta(hours=4, minutes=7), # staggered
            'args'      : ('mlb',),
        },
        'nfl_contest_pool_schedule_manager' : {
            'task' : 'contest.schedule.tasks.contest_pool_schedule_manager',
            'schedule' : timedelta(hours=4, minutes=13), # staggered
            'args'      : ('nfl',),
        },

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

        #
        ########################################################################
        # generate the underlying contests for ContestPools at their start
        ########################################################################
        # checks all sports all sports
        'generate_contest_pool_contests' : {
            'task'      : 'contest.tasks.spawn_contest_pool_contests',
            'schedule'  : timedelta(seconds=60), # every 60 seconds
            #'args'      : ('nba',),
        },

        #
        ########################################################################
        # generate the scheduled blocks for upcoming days
        ########################################################################
        # nba
        'nba_create_scheduled_block_contest_pools' : {
            'task'      : 'contest.schedule.tasks.create_scheduled_contest_pools',
            'schedule'  : timedelta(seconds=60), # every 60 seconds
            'args'      : ('nba',),
        },
        # nhl
        'nhl_create_scheduled_block_contest_pools' : {
            'task'      : 'contest.schedule.tasks.create_scheduled_contest_pools',
            'schedule'  : timedelta(seconds=60), # every 60 seconds
            'args'      : ('nhl',),
        },
        # mlb
        'mlb_create_scheduled_block_contest_pools' : {
            'task'      : 'contest.schedule.tasks.create_scheduled_contest_pools',
            'schedule'  : timedelta(seconds=60), # every 60 seconds
            'args'      : ('mlb',),
        },
        # nfl
        'nfl_create_scheduled_block_contest_pools' : {
            'task'      : 'contest.schedule.tasks.create_scheduled_contest_pools',
            'schedule'  : timedelta(seconds=60), # every 60 seconds
            'args'      : ('nfl',),
        },

        #
        ########################################################################
        # generate salaries each day at 8am (est)
        ########################################################################
        'nba_generate_salaries' : {
            'task'      : 'salary.tasks.generate_salaries_for_sport',
            'schedule'  : crontab(minute=0, hour='14'), # 2 PM (UTC) - which is ~ 9 AM EST
            'args'      : ('nba',),
        },
        'nhl_generate_salaries' : {
            'task'      : 'salary.tasks.generate_salaries_for_sport',
            'schedule'  : crontab(minute=0, hour='14'), # 2 PM (UTC) - which is ~ 9 AM EST
            'args'      : ('nhl',),
        },
        'mlb_generate_salaries' : {
            'task'      : 'salary.tasks.generate_salaries_for_sport',
            'schedule'  : crontab(minute=0, hour='14'), # 2 PM (UTC) - which is ~ 9 AM EST
            'args'      : ('mlb',),
        },
        # nfl done on thursdays only
        'nfl_generate_salaries' : {
            'task'      : 'salary.tasks.generate_salaries_for_sport',
            'schedule'  : crontab(minute=0, day_of_week='thu', hour='14'), # 2 PM (UTC) - which is ~ 9 AM EST
            'args'      : ('nfl',),
        },

        #
        # update injury information for the sports
        'nba_injuries' : {
            'task': 'sports.nba.tasks.update_injuries',
            'schedule': timedelta(minutes=30),
        },

        'nhl_injuries' : {
            'task': 'sports.nhl.tasks.update_injuries',
            'schedule': timedelta(minutes=30),
        },

        'nfl_injuries' : {
            'task': 'sports.nfl.tasks.update_injuries',
            'schedule': timedelta(minutes=30),
        },

        'mlb_injuries' : {
            'task': 'sports.mlb.tasks.update_injuries',
            'schedule': timedelta(minutes=30),
        },

        #
        # update the season_fppg for each sport
        'nba_season_fppg' : {
            'task'      : 'salary.tasks.generate_season_fppgs',
            'schedule'  : crontab(hour='9'), # 9 AM (UTC) - which is ~ 4 AM EST
            'args'      : ('nba',),
        },
        'nhl_season_fppg' : {
            'task'      : 'salary.tasks.generate_season_fppgs',
            'schedule'  : crontab(hour='9'), # 9 AM (UTC) - which is ~ 4 AM EST
            'args'      : ('nhl',),
        },
        'nfl_season_fppg' : {
            'task'      : 'salary.tasks.generate_season_fppgs',
            'schedule'  : crontab(hour='9'), # 9 AM (UTC) - which is ~ 4 AM EST
            'args'      : ('nfl',),
        },
        'mlb_season_fppg' : {
            'task'      : 'salary.tasks.generate_season_fppgs',
            'schedule'  : crontab(hour='9'), # 9 AM (UTC) - which is ~ 4 AM EST
            'args'      : ('mlb',),
        },

        #
        # payout task
        'notify_admin_contests_automatically_paid_out' : {
            'task'      : 'contest.tasks.notify_admin_contests_automatically_paid_out',
            'schedule'  : timedelta(minutes=5),
        },

        # cleanup rosters
        'nba_cleanup_rosters' : {
            'task'      : 'sports.nba.tasks.cleanup_rosters',
            'schedule'  : crontab(hour='3'), # 9 AM (UTC) - which is ~ 4 AM EST
        },
        'nhl_cleanup_rosters' : {
            'task'      : 'sports.nhl.tasks.cleanup_rosters',
            'schedule'  : crontab(hour='3'), # 9 AM (UTC) - which is ~ 4 AM EST
        },
        'nfl_cleanup_rosters' : {
            'task'      : 'sports.nfl.tasks.cleanup_rosters',
            'schedule'  : crontab(hour='3'), # 9 AM (UTC) - which is ~ 4 AM EST
        },
        'mlb_cleanup_rosters' : {
            'task'      : 'sports.mlb.tasks.cleanup_rosters',
            'schedule'  : crontab(hour='3'), # 9 AM (UTC) - which is ~ 4 AM EST
        },
    },

    CELERY_ENABLE_UTC = True,
    CELERY_TIMEZONE = 'UTC',
    CELERY_TRACK_STARTED = True,

    # testing this out, but the BROKER_TRANSPORT_OPTIONS seems to be the
    # setting that actually caps the max connections when were viewing
    # connections on the redis side
    #CELERY_REDIS_MAX_CONNECTIONS = 200,

    #
    #
    # # testing this out
    # BROKER_TRANSPORT_OPTIONS = {
    #     'max_connections': 5,
    # },
    #
    # # None causes a connection to be created and closed for each use
    # BROKER_POOL_LIMIT = None,  # default: 10

)

class locking(object):
    """
    a DECORATOR for locking a task, utilizing the django cache

    usage:

        @app.task(bind=True)
        @locking("lock_prefix", 30)       #
        def some_task(a1, a2, a3, a4):
            print('sayHello arguments:', a1, a2, a3, a4)

    """

    def __init__(self, unique_lock_name, timeout):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        #print("Inside __init__()")
        self.unique_lock_name       = unique_lock_name
        self.timeout                = timeout

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """

        def wrapped_f(*args):
            #print("Decorator arguments:", self.unique_lock_name, self.timeout)

            # the redis lock is blocking, and will auto-release
            with redis.Redis().lock(self.unique_lock_name, timeout=self.timeout):
                # call the function this decorator is decorating!
                return f(*args)

        return wrapped_f # return the return vlue of our wrapped method if there are any

class TaskHelper(object):
    """
    primarily responsible for retrieving the result of a task,
    which is typically None if successful, but may also
    return the exception which caused the task to fail
    """

    # these are our own statuses, not the task.status values
    SUCCESS = 'SUCCESS'
    PENDING = 'PENDING'
    FAILURE = 'FAILURE'
    statuses = [
        SUCCESS,
        PENDING,
        FAILURE
    ]
    final_statuses = [
        SUCCESS,
        FAILURE
    ]
    pending_statuses = [
        PENDING
    ]

    def __init__(self, t, task_id):
        self.t          = t
        self.task_id    = task_id
        self.task       = t.AsyncResult( task_id )

    def get_task_data(self):
        """
        get the task's status and a note about what its status means
        :return:
        """

        status = self.task.status
        return {
            'status' : status,
            'description' : self.get_status_description(status)
        }

    def get_status_description(self, status):
        """
        return a string description of what the task status indicates.

        Assumes the status will be in, otherwise returns an Unkonwn celery state description.
            {'FAILURE',
               'PENDING',
               'RECEIVED',
               'RETRY',
               'REVOKED',
               'STARTED',
               'SUCCESS'})

        :param status:
        :return:
        """

        if status not in celery.states.ALL_STATES:
            return '%s - Unknown celery state!' % status

        if status == 'PENDING':
            return 'Task state is unknown (assumed pending since you know the id).'
        elif status == 'RECEIVED':
            return 'Task was received by a worker.'
        elif status == 'STARTED':
            return 'Task was started by a worker (CELERY_TRACK_STARTED).'
        elif status == 'SUCCESS':
            return 'Task succeeded'
        elif status == 'FAILURE':
            return 'Task failed'
        elif status == 'REVOKED':
            return 'Task was revoked.'
        elif status == 'RETRY':
            return 'Task is waiting for retry'

    def get_note(self):
        """
        :return: string note about the data returned.
        """
        fmt_str = 'status will be in %s. if status is in %s, you may poll this api.'
        s = fmt_str% (str(self.statuses), str(self.pending_statuses))
        return s

    def get_overall_status(self):
        """
        for any task status other than SUCCESS or FAILURE, return PENDING
        :return:
        """
        if self.task.status in self.final_statuses:
            return self.task.status
        else:
            return self.PENDING

    def get_data(self):
        """
        return information about the task result,
        specifically return the task state, along with the exception class name,
        and message if there was an exception.

        :return: {'task_status': <task-status>, 'exception': None}
                    ... or ...
                 {'task_status': <task-status>,
                    'exception': {
                        'name': 'Exception',
                        'msg' : 'the exceptions string message',
                     }
                 }
        """

        # defaults
        exception   = None
        result      = None
        r           = self.task.result

        if r is not None and issubclass(type(r), Exception):
            #
            # return exception information here, including class name, and msg
            exception = {
                'name' : type(r).__name__,   # ie: 'Exception'
                'msg'   : str(r)
            }

        else:
            #
            # if you want to return valid data returned by the task, do it here
            result = {
                'value' : r, # a sucessful task may return None, or possibly an object
            }

        # the top-level 'status' is not the task status, it
        # is a more general indication of the success/pending/failure
        data = {
            'task_id'       : self.task_id,
            'status'        : self.get_overall_status(),
            'note'          : self.get_note(),
            'task'          : self.get_task_data(),

            # 'exception' OR 'result' will be set upon SUCCESS/FAILURE.
            # it is possible that the 'result' will have a null value
            # in it if the task is successful but simply had no return value!
            'exception'     : exception,
            'result'        : result,
        }
        return data

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

@app.task(bind=True)
def save_model_instance(self, instance):
    """
    calls save() on a model instance
    """
    LOCK_EXPIRE_SECONDS = 5
    # The cache key consists of the task name and the MD5 digest of the sport
    lock_id = 'LOCK-save-{0}-{1}'.format(str(type(instance)), str(instance.pk))
    # cache.add fails if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 1, LOCK_EXPIRE_SECONDS)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            # call save() on the instance
            instance.save()
        finally:
            release_lock()
    else:
        pass # if it couldnt aquire the lock thats really too bad, isnt it?...
