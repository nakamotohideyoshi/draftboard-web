from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.deletion import Collector

TRANSACTION_CATEGORY = (
    ('contest-buyin', 'Contest Buyin'),
    ('contest-payout', 'Contest Payout'),
    ('funds-deposit', 'Funds Deposit'),
    ('funds-withdrawal', 'Funds Withdrawal'),
    # ('xxx', 'Xxx'),
    # ('xxx', 'Xxx'),
    # ('xxx', 'Xxx'),
)


class AbstractAmount(models.Model):
    def get_category(self):
        # should return "CashAmount", or "TicketAmount", etc...
        raise Exception(
            'inheriting class must implement this method: transaction.models.AbstractAmount.get_amount_type()')

    def get_transaction_class(self):
        raise Exception(
            'inheriting class must implement this method: transaction.models.AbstractAmount.get_transaction_class()')

    def get_cash_value(self):
        raise Exception(
            'inheriting class must implement this method: transaction.models.AbstractAmount.get_cash_value()')

    class Meta:
        abstract = True


class TransactionType(models.Model):
    """
    The class that keeps a list of all the transaction
    types/actions and their corresponding string representation.
    """
    category = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('category', 'name')

    def to_json(self):
        return {
            'category': self.category,
            'name': self.name,
            'description': self.description,
        }

    def __str__(self):
        return '%s  %s' % (self.category, self.name)


class Transaction(models.Model):
    """
    This class keeps track of all
    """

    JSON_CONTEST_FIELD = 'contest'

    category = models.ForeignKey(TransactionType)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s  %s  %s' % (self.created.date(), self.user, self.category)

    def to_json(self):
        collector = Collector(using='default')  # or specific database
        collector.collect([self])
        array = []

        buyin_ctype = ContentType.objects.get(app_label='buyin', model='buyin')
        buyin_model_class = buyin_ctype.model_class()
        payout_ctype = ContentType.objects.get(app_label='payout', model='payout')
        payout_model_class = payout_ctype.model_class()
        # buyins = buyin_model_class.objects.all()

        for model_tmp, instance_tmp in collector.instances_with_model():
            if hasattr(instance_tmp,
                       "to_json") and instance_tmp != self and instance_tmp.user == self.user:
                array.append(instance_tmp.to_json())

        data = {
            "created": str(self.created),
            "details": array,
            "id": self.pk,
            self.JSON_CONTEST_FIELD: None,
        }

        buyin = None
        try:
            buyin = buyin_model_class.objects.get(transaction_id=self.pk)
            data[self.JSON_CONTEST_FIELD] = buyin.contest.pk
        except:
            pass

        if buyin is None:
            # it must be a payout
            try:
                payout = payout_model_class.objects.get(transaction_id=self.pk)
                data[self.JSON_CONTEST_FIELD] = payout.contest.pk
            except:
                pass

        # return the json
        return data


class TransactionDetail(models.Model):
    """
    The base model for the classes to keep track of
    the transactions.
    """
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    user = models.ForeignKey(User)
    transaction = models.ForeignKey(Transaction, null=False, related_name='+')
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('user', 'transaction')

    def to_json(self):
        return {
            "created": str(self.created),
            "amount": self.amount,
            "type": self.__class__.__name__,
            "id": self.pk,
            'category': self.transaction.category.to_json()

        }


class Balance(models.Model):
    """
    The base model for classes to maintain a balance based
    off the TransactionDetail.

    """
    user = models.OneToOneField(User, primary_key=True)
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
