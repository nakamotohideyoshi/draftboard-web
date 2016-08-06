#
# tax/classes.py

from mysite.classes import AbstractSiteUserClass
from .models import Tax
from cash.models import CashTransactionDetail
from django.utils import timezone
from django.contrib.auth.models import User
from transaction.models import Transaction
from django.db.models import F, FloatField, Sum
from django.contrib.contenttypes.models import ContentType

class TaxManager(AbstractSiteUserClass):

    def __init__(self, user):
        super().__init__(user)

    def info_collected(self):
        # TODO this needs to be stored elsewhere
        """

        :return: whether the information for taxes has been collected
        """
        try:
            Tax.objects.get(user=self.user)
        except Tax.DoesNotExist:
            return False
        return True

    def set_tax_id(self, tax_id):
        try:
            tax = Tax.objects.get(user=self.user)
        except Tax.DoesNotExist:
            tax  = Tax()
            tax.user = self.user
        tax.tax_identifier = tax_id
        tax.save()

    def sum_transactions_for_model(self, model_class, transactions, contest_isnull=False):
        """
        method returns a dict like this: {'amount__sum': Decimal('-5075.00')}

        :param model_class: ie: Buyin, Payout, etc...
        :param transactions: the base transactions the model_class instances point to
        :return:
        """
        models = model_class.objects.filter(transaction__in=transactions,
                                             contest__isnull=contest_isnull)

        model_transactions = []
        for m in models:
            model_transactions.append(m.transaction)
        details = CashTransactionDetail.objects.filter(
                        transaction__in=model_transactions, user=self.user).aggregate(Sum('amount'))
        #print(str(details))
        amount = details.get('amount__sum', 0)
        if amount is None:
            amount = 0
        #print(amount)
        return amount

    def calendar_year_net_profit(self):
        net_profit = 0
        now = timezone.now()
        jan1 = now.replace(now.year, 1, 1, 0, 0, 0)  # does not side-effect 'now'
        transactions = Transaction.objects.filter(user=self.user,
                                    created__range=(jan1, now)).order_by('-created')
        # get the buyin amount sum for these transactions
        buyin_ctype = ContentType.objects.get(app_label='buyin', model='buyin')
        buyin_model_class = buyin_ctype.model_class()
        # method returns a dict like this: {'amount__sum': Decimal('-5075.00')}
        buyins = self.sum_transactions_for_model(buyin_model_class, transactions)
        net_profit += buyins

        # get the payout amount sum for these transactions
        payout_ctype = ContentType.objects.get(app_label='payout', model='payout')
        payout_model_class = payout_ctype.model_class()
        payouts = self.sum_transactions_for_model(payout_model_class, transactions)
        net_profit += payouts

        return net_profit







