from __future__ import absolute_import

#
# account/tasks.py

from mysite import celery_app as app
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.db.models import Q

from contest.models import Entry
# /password/reset/confirm/{uid}/{token}

def encode_uid(pk):
    try:
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes
        return urlsafe_base64_encode(force_bytes(pk)).decode()
    except ImportError:
        from django.utils.http import int_to_base36
        return int_to_base36(pk)

#
# example password reset link
# https://www.draftboard.com/api/account/password-reset-confirm/MjA0/47k-95ee193717cb75448cf0/

@app.task(bind=True)
def send_password_reset_email(self, user, https=True):
    #raise Exception('UNIMPLEMENTED - account.tasks.send_password_reset_email')
    token       = default_token_generator.make_token(user)
    uid         = encode_uid(user.pk)
    site        = settings.SITE
    protocol    = 'https' if https else 'http'
    url         = '%s://%s/api/account/password-reset-confirm/%s/%s/' % (protocol, site, uid, token)
    print( url )
    send_mail('password reset email', 'hey, heres your password reset link: ' + url, settings.DEFAULT_FROM_EMAIL, [user.email])


@app.task
def inactive_users_email(users):
    if settings.INACTIVE_USERS_EMAILS:
        subject = 'Inactive users'
        body = settings.SITE + reverse('admin:auth_user_changelist') + '?id__in=' + ','.join([str(x.id) for x in users])
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, settings.INACTIVE_USERS_EMAILS)



@app.task(bind=True)
def check_not_active_users(self):
    day = timezone.now() - timezone.timedelta(days=180)
    # get last user entry, then filter them
    entries_users = Entry.objects.all().order_by('user', '-created').distinct('user').filter(created__lt=day).\
        values_list('user_id', flat=True)
    users = User.objects.filter(cashbalance__amount__gte=5, information__inactive=False).\
        filter(Q(last_login__lt=day) | Q(id__in=entries_users))
    if users.exists():
        inactive_users_email.delay(users)
    users.update(inactive=True)
