from __future__ import absolute_import

from mysite.celery_app import app
from .classes import RefundManager
from django.core.cache import cache
from .exceptions import ContestRefundInProgressException
LOCK_EXPIRE = 60*10 # Lock expires in 10 minutes
SHARED_LOCK_NAME = "refund_task"

@app.task(bind=True)
def refund_task(self, contest):
    lock_id = '%s-LOCK-contest[%s]'%(SHARED_LOCK_NAME, contest.pk)

    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            rm = RefundManager()
            rm.refund(contest)
        finally:
            release_lock()
    else:
        raise ContestRefundInProgressException()


