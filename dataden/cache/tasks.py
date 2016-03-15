from __future__ import absolute_import

#
# dataden/cache/tasks.py

from django.conf import settings
from django.core.cache import cache
from mysite.celery_app import app

LOCK_EXPIRE                 = 15 # seconds before lock expires
TASK_LOCK_PREFIX            = 'countdown_to_combine_pbp_stats_task-LOCK'

@app.task(bind=True)
def countdown_to_combine_pbp_stats_task(self, linkable_player_object, queue_table):
    """
    this task delays for a configured amount of time, and then
    """

    # create anonymous functions basically for getting and relinquishing a lock
    player_srid = linkable_player_object.get_srid()
    lock = '%s-%s' % (TASK_LOCK_PREFIX, player_srid)
    acquire_lock = lambda: cache.add(lock, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock)

    if acquire_lock(): # we want a lock on the thing that fires the task so we never duplicated
        try:
            pass
        finally:
            release_lock()
    else:
        pass # lock couldnt be had,