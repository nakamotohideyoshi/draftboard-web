#
# push/tasks.py

from __future__ import absolute_import

from mysite.celery_app import app, locking
from django.core.cache import cache
import redis

PUSH_TASKS_STATS_LINKER = 'push_tasks_stats_linker'

@app.task(bind=True)
def pusher_send_task(self, pushable, data):
    pushable.trigger( data )

@app.task(bind=True)
def linker_pusher_send_task(self, pushable, data, identifier):
    # TODO - blocking lock on the PUSH_TASKS_STATS_LINKER with redis mechanims in @mysite.celery_app.locking

    # atomically delete the identifier from the cache.
    # delete() returns > 0 if it deleted something.
    # if it didnt, that means no identifier existed,
    # and that means we dont need to send the data.
    if cache.delete(identifier) == 0:
        print('... dont need to send data, no cache token:', str(data))
        return # the identifier token didnt exist, so we dont need to send it
    else:
        print('... need to send data:', str(data))

    # now we know we have to send the data, since we deleted something
    pushable.trigger( data )

    # TODO - remove the object with the identifier from the linked queue in the cache too!



