from __future__ import absolute_import

#
# refund/tasks.py

from mysite.celery_app import app
from .classes import RefundManager
from django.core.cache import cache
from contest.models import LiveContest
from .exceptions import ContestRefundInProgressException
import contest.buyin.tasks

LOCK_EXPIRE = 60  # seconds
SHARED_LOCK_NAME = "refund_task"

@app.task(bind=True)
def refund_task(self, contest, force=False, admin_force=False):
    lock_id = '%s-LOCK-contest[%s]'%(SHARED_LOCK_NAME, contest.pk)

    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            rm = RefundManager()
            rm.refund(contest, force=force, admin_force=admin_force)
        finally:
            release_lock()
    else:
        raise ContestRefundInProgressException()

@app.task(bind=True)
def refund_and_cancel_live_contests_task(self, debug=False):
    """
    This task will only cancel contests where: current entries < total entries

    This task will only refund and cancel entries in LiveContest which are NON-Gpp Contests
    and which did not fill reach the maximum entries.

    :return:
    """

    contests_to_cancel = {}
    for contest in LiveContest.objects.all():
        # TODO - for now, we have decided to simply
        #        cancel any game that has less entries
        #        than payout spots!
        if contest.current_entries < contest.prize_structure.payout_spots:
            contests_to_cancel[ contest.pk ] = True
            refund_task.delay( contest, force=True, admin_force=True )  # admin_force=True is not a typical situation!

    contests = LiveContest.objects.filter(gpp=False)
    for contest in contests:
        if contest.current_entries < contest.entries:
            contests_to_cancel[ contest.pk ] = True
            refund_task.delay( contest, force=True )
    if debug:
        contests_to_cancel_list = [ int(x) for x in contests_to_cancel.keys() ]
        print( str(contests_to_cancel_list) )

@app.task(bind=True, time_limit=20, soft_time_limit=10)
def unregister_entry_task(self, entry):
    """
    it is paramount this task uses the same lock as the buyin_task because
    both tasks manipulate contest entries!

    :param entry:
    :return:
    """

    lock_expire = contest.buyin.tasks.LOCK_EXPIRE
    lock_id     = contest.buyin.tasks.SHARED_LOCK_FORMAT % (entry.contest.pk)

    acquire_lock = lambda: cache.add(lock_id, 'true', lock_expire)
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            bm = RefundManager()
            bm.remove_and_refund_entry(entry)
        finally:
            release_lock()
    else:
        self.retry(countdown=1, max_retries=20)





