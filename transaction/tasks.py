from __future__ import absolute_import

from django.template.loader import render_to_string

from mysite import celery_app as app
from mysite.utils import send_email


@app.task
def send_deposit_receipt(user, amount, balance, transaction_date):
    subject = 'Deposit receipt'

    ctx = {
        'username': user.username,
        'amount': amount,
        'balance': balance,
        'date': transaction_date,
    }

    message = render_to_string('account/emails/deposit_receipt.html', ctx)

    send_email(
        subject=subject,
        recipients=[user.email],
        title=subject,
        message=message,
    )
