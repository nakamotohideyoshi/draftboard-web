from __future__ import absolute_import

from django.core.cache import cache

import contest.buyin.tasks
from mysite.celery_app import app
from .classes import RefundManager
from .exceptions import (ContestRefundInProgressException, UnmatchedEntryRefundInProgressException)

LOCK_EXPIRE = 60  # seconds
SHARED_LOCK_NAME = "refund_task"


@app.task(bind=True)
def refund_task(self, contest, force=False, admin_force=False):
    """
    :param self:
    :param contest:
    :param force:
    :param admin_force:
    :return:
    """
    lock_id = '%s-LOCK-contest[%s]' % (SHARED_LOCK_NAME, contest.pk)

    def acquire_lock():
        return cache.add(lock_id, 'true', LOCK_EXPIRE)

    def release_lock():
        return cache.delete(lock_id)

    if acquire_lock():
        try:
            rm = RefundManager()
            rm.refund(contest, force=force, admin_force=admin_force)
        finally:
            release_lock()
    else:
        raise ContestRefundInProgressException()


@app.task(bind=True, time_limit=20, soft_time_limit=10)
def unregister_entry_task(self, entry):
    """
    it is paramount this task uses the same lock as the buyin_task because
    both tasks manipulate contest entries!

    :param entry:
    :return:
    """

    lock_expire = contest.buyin.tasks.LOCK_EXPIRE
    lock_id = contest.buyin.tasks.SHARED_LOCK_FORMAT % entry.contest_pool.pk

    def acquire_lock():
        return cache.add(lock_id, 'true', LOCK_EXPIRE)

    def release_lock():
        return cache.delete(lock_id)

    if acquire_lock():
        try:
            bm = RefundManager()
            bm.remove_and_refund_entry(entry)
        finally:
            release_lock()
    else:
        self.retry(countdown=1, max_retries=20)


@app.task(bind=True)
def refund_unmatched_entry(self, entry):
    """
    This is just a celery task wrapper for RefundManager.refund_unmatched_entry.

    :param self: Task instance.
    :param entry: The entry to refund.
    """
    lock_id = '%s-LOCK-contest[%s]' % (SHARED_LOCK_NAME, entry.pk)

    def acquire_lock():
        return cache.add(lock_id, 'true', LOCK_EXPIRE)

    def release_lock():
        return cache.delete(lock_id)

    if acquire_lock():
        try:
            rm = RefundManager()
            rm.refund_unmatched_entry(entry)
        finally:
            release_lock()
    else:
        raise UnmatchedEntryRefundInProgressException(entry)
