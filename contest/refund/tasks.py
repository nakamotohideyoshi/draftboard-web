from __future__ import absolute_import

from mysite.celery_app import app
from .classes import RefundManager
from django.core.cache import cache
from contest.models import LiveContest
from .exceptions import ContestRefundInProgressException

LOCK_EXPIRE = 60  # seconds
SHARED_LOCK_NAME = "refund_task"

@app.task(bind=True)
def refund_task(self, contest, force=False):
    lock_id = '%s-LOCK-contest[%s]'%(SHARED_LOCK_NAME, contest.pk)

    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            rm = RefundManager()
            rm.refund(contest, force=force)
        finally:
            release_lock()
    else:
        raise ContestRefundInProgressException()

@app.task(bind=True)
def refund_and_cancel_live_contests_task(self):
    """
    This task will only cancel contests where: current entries < total entries

    This task will only refund and cancel entries in LiveContest which are NON-Gpp Contests
    and which did not fill reach the maximum entries.

    :return:
    """

    contests = LiveContest.objects.all()
    for contest in contests:
        if contest.current_entries < contest.entries:
            refund_task.delay( contest, force=True )




