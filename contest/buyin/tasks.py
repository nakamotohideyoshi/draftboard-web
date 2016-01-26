from __future__ import absolute_import

from mysite.celery_app import app
from .classes import BuyinManager
from django.core.cache import cache

LOCK_EXPIRE = 30 # Lock expires in 5 minutes
SHARED_LOCK_NAME = "buyin_task"

@app.task(bind=True, time_limit=20, soft_time_limit=10)
def buyin_task(self, user, contest, lineup=None):
    lock_id = '%s-LOCK-contest[%s]'%(SHARED_LOCK_NAME, contest.pk)

    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            bm = BuyinManager(user)
            bm.buyin(contest, lineup)
        finally:
            release_lock()
    else:
        self.retry(countdown=1, max_retries=100)




