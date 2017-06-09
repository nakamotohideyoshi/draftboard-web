from __future__ import absolute_import

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail

from cash.withdraw.models import PayPalWithdraw
from mysite.celery_app import app

# emails to receive Withdraw request emails
EMAILS = [
    'devs@draftboard.com',
    'manager@draftboard.com',
]

LOCK_EXPIRE = 60  # lock expires in this many seconds
SHARED_LOCK_NAME = 'withdraw_request_emails'


@app.task(bind=True)
def notify_recent_withdraws(self):
    """
    email the neccessary people with information about recent withdraws
    """
    lock_id = 'task-LOCK--%s--%s' % ('all_sports', SHARED_LOCK_NAME)

    acquire_lock = lambda: cache.add(lock_id, 'lock', LOCK_EXPIRE)
    release_lock = lambda: cache.delete(lock_id)

    withdraws = PayPalWithdraw.objects.filter(status__category__in=['Pending'])
    if withdraws.count() == 0:
        return  # not notifications required if there arent any

    if acquire_lock():
        try:
            subject = 'Draftboard has %s Pending Withdraws.' % (withdraws.count())
            body = 'heres the link: %s/admin/withdraw/paypalwithdraw/' % settings.DOMAIN
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, EMAILS)

        finally:
            release_lock()
