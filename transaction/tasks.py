from __future__ import absolute_import

from mysite import celery_app as app
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


@app.task
def send_deposit_receipt(transaction, amount, transaction_date):
    subject = 'Deposit receipt'
    ctx = {
        'username': transaction.user.username,
        'amount': amount,
        'balance': transaction.balance.amount,
        'date': transaction_date,
    }

    message = render_to_string('account/emails/deposit_receipt.html', ctx)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [transaction.user.email])