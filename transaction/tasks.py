from __future__ import absolute_import

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from mysite import celery_app as app


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

    send_mail(
        subject=subject,
        message=message,
        html_message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[transaction.user.email],
    )
