from __future__ import absolute_import

from mysite.celery_app import app
from .watcher import Trigger
from django.conf import settings
import subprocess
from django.core.cache import cache
from celery.task.control import inspect

LOCK_EXPIRE = 30 # seconds before lock expires

TASK_LOCK_DATADEN           = 'TASK_LOCK_DATADEN'
TASK_LOCK_DATADEN_TRIGGER   = 'TASK_LOCK_DATADEN_TRIGGER'

# @app.task(bind=True)
# def buyin_task(self, user, contest, lineup=None):
#     lock_id = '%s-LOCK-contest[%s]'%(SHARED_LOCK_NAME, contest.pk)
#
#     acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
#     release_lock = lambda: cache.delete(lock_id)
#
#     if acquire_lock():
#         try:
#             bm = BuyinManager(user)
#             bm.buyin(contest, lineup)
#         finally:
#             release_lock()
#     else:
#         self.retry(countdown=1, max_retries=100)

@app.task(bind=True)
def dataden(self):
    """
    run dataden jar via command line, in a single task and make sure
    we get a lock so it would be impossible to run two dataden
    instances at the same time.

    :return:
    """

    # create anonymous functions basically for getting and relinquishing a lock
    acquire_lock = lambda: cache.add(TASK_LOCK_DATADEN, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(TASK_LOCK_DATADEN)

    if acquire_lock(): # we want a lock on the thing that fires the task so we never duplicated
        try:
            i = inspect()
            active_tasks = i.active()
            # {'celery@vagrant-ubuntu-trusty-64':
            #      [
            #        {'worker_pid': 17882,
            #        'args': '[]',
            #        'kwargs': '{}',
            #        'time_start': 1575959.732842815,
            #        'acknowledged': True,
            #        'delivery_info': {'priority': 0,
                #         'exchange': 'celery',
                #         'redelivered': None,
                #         'routing_key': 'celery'},
            #        'name': 'dataden.tasks.dataden_runner',
            #        'hostname': 'celery@vagrant-ubuntu-trusty-64',
            #        'id': '9eb99e90-d862-4f2c-87de-27893ede9713'
            #         }
            #      ]
            # }
            found = False
            for worker, running in active_tasks.items():
                for t in running:
                    if t.get('name') == dataden_runner.name: # compare with the name of the task
                        found = True
                        break
                if found: break # get out of the outter loop too, if it was found
            #
            # only fire it if it was not running
            if not found:
                # START DATADEN PROCESS
                dataden_runner.apply_async( queue='q_dataden')
            else:
                print( '... monitoring dataden: its running.')

        finally:
            release_lock()
    else:
        pass # lock couldnt be had,

@app.task(bind=True)
def dataden_runner(self):
    print( 'starting dataden, because it was not already running!')
    cmd_str = 'java -jar dataden/dataden-rio.jar -k %s -q' % settings.DATADEN_LICENSE_KEY
    command = cmd_str.split()
    popen = subprocess.Popen(command, stdout=subprocess.PIPE)
    lines_iterator = iter(popen.stdout.readline, b"")
    for line in lines_iterator:
        print(line) # yield line

@app.task(bind=True)
def dataden_trigger(self):
    """
    run dataden triggers on the mongo database

    :return:
    """

    acquire_lock = lambda: cache.add(TASK_LOCK_DATADEN_TRIGGER, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(TASK_LOCK_DATADEN_TRIGGER)

    if acquire_lock(): # we want a lock on the thing that fires the task so we never duplicated
        try:
            i = inspect()
            active_tasks = i.active()
            found = False
            for worker, running in active_tasks.items():
                for t in running:
                    if t.get('name') == dataden_trigger_runner.name: # compare with the name of the task
                        found = True
                        break
                if found: break # get out of the outter loop too, if it was found
            #
            # only fire it if it was not running
            if not found:
                # START DATADEN TRIGGER PROCESS
                dataden_trigger_runner.apply_async(queue='q_dataden_trigger')
            else:
                print( '... monitoring dataden_trigger: its running.')

        finally:
            release_lock()
    else:
        pass # lock couldnt be had, which means something else was run

@app.task(bind=True)
def dataden_trigger_runner(self):
    print("starting dataden_trigger")
    trigger = Trigger()
    trigger.run()


