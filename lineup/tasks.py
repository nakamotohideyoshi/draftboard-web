from __future__ import absolute_import

from mysite.celery_app import app
from .classes import LineupManager
from celery import task
from django.core.cache import cache
from .exceptions import  EditLineupInProgressException

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes
SHARED_LOCK_NAME = "lineup"
@app.task
def edit_lineup(user, player_ids, lineup):
    def edit_lineup_subtask(u, p, l):
        lm = LineupManager(u)
        lm.edit_lineup(p, l)
    run_lineup_task(user, edit_lineup_subtask, user, player_ids, lineup)


@app.task
def edit_entry(user, player_ids, entry):
    def edit_entry_subtask(u, p, e):
        lm = LineupManager(u)
        lm.edit_entry(p, e)
    run_lineup_task(user, edit_entry_subtask, user, player_ids, entry)

def run_lineup_task(user, method, *args, **kwargs ):
    lock_id = '%s-LOCK-user[%s]'%(SHARED_LOCK_NAME, user.pk)

    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            method(*args, **kwargs)

        finally:
            release_lock()
    else:
        raise EditLineupInProgressException()
