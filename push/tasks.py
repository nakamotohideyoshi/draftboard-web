from __future__ import absolute_import

from django.core.cache import cache

from mysite.celery_app import app

# from dataden.util.hsh import Hashable

#
# this is the lock key used by the following objects:
#
#   1.  push.classes.AbstractPush to linke pbp+stats
#   2.  push.tasks.linker_pusher_send_task
#
#  ... you should not use it, or stop things from using
# it unless you specifically know what you are doing.
PUSH_TASKS_STATS_LINKER = 'push_tasks_stats_linker'


@app.task(bind=True)
def pusher_send_task(self, pushable, data):
    # print('pusher_send_task ::', str(data))
    pushable.trigger(data)


@app.task(bind=True)
def linker_pusher_send_task(self, pushable, data, identifier):
    # TODO - blocking lock on the PUSH_TASKS_STATS_LINKER with redis
    # mechanisms in @mysite.celery_app.locking

    # atomically delete the identifier from the cache.
    # delete() returns > 0 if it deleted something.
    # if it didnt, that means no identifier existed,
    # and that means we dont need to send the data.

    cdelete = cache.delete(identifier)
    print('cdelete: %s' % str(cdelete))
    if cdelete == 0:
        print('... dont need to send data, no cache token:', str(data))
        return  # the identifier token didnt exist, so we dont need to send it
    else:
        print('... need to send data:', str(data))

    # now we know we have to send the data, since we deleted something
    if not isinstance(data, dict):
        data = data.get_o()
    pushable.trigger(data)

    # TODO - remove the object with the identifier from the linked queue in the cache too!
