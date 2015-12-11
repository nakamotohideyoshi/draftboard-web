from __future__ import absolute_import

#
# account/tasks.py

from mysite import celery_app as app
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
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