from __future__ import absolute_import

from mysite.celery_app import app
from .classes import PayoutManager
from django.core.cache import cache

LOCK_EXPIRE = 300 # Lock expires in 5 minutes
SHARED_LOCK_NAME = "payout_task"

@app.task(bind=True)
def payout_task(self, contests=None):
    lock_id = '%s-LOCK-payout[%s]'

    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            pm = PayoutManager()
            pm.payout(contests)
        finally:
            release_lock()
    else:
        self.retry(countdown=1, max_retries=100)



