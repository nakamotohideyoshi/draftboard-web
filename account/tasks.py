from __future__ import absolute_import

from logging import getLogger

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import timezone

from account.models import (
    Information,
    Identity,
)
from contest.models import Entry
from mysite import celery_app as app
from .utils import encode_uid

logger = getLogger('account.tasks')


# example password reset link
# https://www.draftboard.com/api/account/password-reset-confirm/MjA0/47k-95ee193717cb75448cf0/
@app.task(bind=True)
def send_password_reset_email(self, user, https=True):
    # raise Exception('UNIMPLEMENTED - account.tasks.send_password_reset_email')
    token = default_token_generator.make_token(user)
    uid = encode_uid(user.pk)
    site = settings.SITE
    protocol = 'https' if https else 'http'
    url = '%s://%s/api/account/password-reset-confirm/%s/%s/' % (protocol, site, uid, token)
    send_mail('password reset email', 'hey, heres your password reset link: ' + url,
              settings.DEFAULT_FROM_EMAIL, [user.email])


@app.task
def inactive_users_email(users):
    if settings.INACTIVE_USERS_EMAILS:
        subject = 'Inactive users'
        body = settings.SITE + reverse('admin:auth_user_changelist') + '?id__in=' + ','.join(
            [str(x.id) for x in users])
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, settings.INACTIVE_USERS_EMAILS)


@app.task(bind=True)
def check_not_active_users(self):
    day = timezone.now() - timezone.timedelta(days=180)
    # get last user entry, then filter them
    entries_users = Entry.objects.all().order_by('user', '-created').distinct('user').filter(
        created__lt=day). \
        values_list('user_id', flat=True)
    users = User.objects.filter(cashbalance__amount__gte=5, information__inactive=False). \
        filter(Q(last_login__lt=day) | Q(id__in=entries_users))
    if users.exists():
        inactive_users_email.delay(users)
        Information.objects.filter(user__in=users).update(inactive=True)


@app.task(bind=True)
def send_entry_alert_email(self, user):
    # TODO: Make this account limit email alert nicer.
    send_mail(
        'entry alert',
        'hey, you have reached your entry alert: ',
        settings.DEFAULT_FROM_EMAIL,
        [user.email]
    )


@app.task
def flagged_identities_email():
    """
    Look for any flagged Trulioo Identities, if any exist, send an email so they can
    be manually investigated.

    Returns: Int Number of Identitiesfound.
    """
    if settings.FLAGGED_IDENTITY_EMAIL_RECIPIENTS:
        flagged_identities = Identity.objects.filter(flagged=True).count()

        if flagged_identities > 0:
            logger.info('Sending email for %s flagged identities.' % flagged_identities)
            subject = 'Flagged Identities'

            body = """
            There are %s flagged identities. Go check them out here: <a href="%s">%s</a>
            """ % (
                flagged_identities,
                settings.SITE + '/admin/account/identity/?flagged__exact=1',
                settings.SITE + '/admin/account/identity/?flagged__exact=1'
            )

            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                      settings.FLAGGED_IDENTITY_EMAIL_RECIPIENTS)
        else:
            logger.info('No flagged identities found, not sending email.')
        # Return a count of flagged identities.
        return flagged_identities
    else:
        logger.info('No FLAGGED_IDENTITY_EMAIL_RECIPIENTS setting, not attempting to send email.')
