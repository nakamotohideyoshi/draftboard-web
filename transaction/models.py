from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.functional import cached_property

from mysite.utils import format_currency


class AbstractAmount(models.Model):
    def get_category(self):
        # should return "CashAmount", or "TicketAmount", etc...
        raise Exception(
            'inheriting class must implement this method: '
            'transaction.models.AbstractAmount.get_amount_type()')

    def get_transaction_class(self):
        raise Exception(
            'inheriting class must implement this method: '
            'transaction.models.AbstractAmount.get_transaction_class()')

    def get_cash_value(self):
        raise Exception(
            'inheriting class must implement this method: '
            'transaction.models.AbstractAmount.get_cash_value()')

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
        return '%s - %s' % (self.category, self.name)


class Transaction(models.Model):
    """
    This class keeps track of all
    """

    category = models.ForeignKey(TransactionType)
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '<Transaction id: %s | created: %s | user: %s | category: %s>' % (
            self.id, self.created.date(), self.user, self.category)

    @cached_property
    def action(self):
        try:
            return self.buyin
        except ObjectDoesNotExist:
            pass
        try:
            return self.payout
        except ObjectDoesNotExist:
            pass
        try:
            return self.refund
        except ObjectDoesNotExist:
            pass
        try:
            return self.rake
        except ObjectDoesNotExist:
            pass
        try:
            return self.fpp
        except ObjectDoesNotExist:
            pass
        return None

    @cached_property
    def user_transaction_details(self):
        """
        This is used to get the transacion details thet are pertinent to the user.
        These get displayed on the account transactions page.
        """
        details = []
        transaction_detail_types = [
            'bonuscashtransactiondetail_set',
            'cashtransactiondetail_set',
            # Ignore any FPP transactions since we don't really use it right now.
            # 'fpptransactiondetail_set',
            # We don't want to show any rakepaid transaction details here.
            # 'rakepaidtransactiondetail_set',
        ]

        for detail_type in transaction_detail_types:
            details += getattr(self, detail_type).filter(user=self.user)

        return details

    @cached_property
    def all_transaction_details(self):
        """
        This will get ALL of the TransactionDetails for this transaciton.
        For instance: if this transaction is a contest buyin, there will be a withdraw
        from the user's account, and a deposit into the escrow account.
        """
        details = []
        transaction_detail_types = [
            'bonuscashtransactiondetail_set',
            'cashtransactiondetail_set',
            'fpptransactiondetail_set',
            'rakepaidtransactiondetail_set',
        ]

        for detail_type in transaction_detail_types:
            details += getattr(self, detail_type).all()

        return details

    def to_json(self, user_only=False):
        data = {
            "created": str(self.created),
            "details": [],
            "action": {},
            "id": self.pk,
            "description": "",
            "contest": None,
            "contest_pool": None,
        }

        if user_only:
            # Add all of the TransactionDetails that include the transaction's user.
            for detail in self.user_transaction_details:
                data['details'].append(detail.to_json())
        else:
            # Add ALL of the TransactionDetails .
            for detail in self.all_transaction_details:
                data['details'].append(detail.to_json())

        # Add Action info and build a description.
        if self.action:
            if hasattr(self.action, "to_json"):
                data['action'] = self.action.to_json()

                # If we have contest info, add that.
                if hasattr(self.action, 'contest') and self.action.contest:
                    data['contest'] = self.action.contest.name
                    data['description'] = "%s for %s entry" % (
                        data['action']['type'], self.action.contest.name)
                # Try to add contest_pool info also.
                if hasattr(self.action, 'contest_pool') and self.action.contest_pool:
                    data['contest_pool'] = self.action.contest_pool.name
                    data['description'] = "%s for %s entry" % (
                        data['action']['type'], self.action.contest_pool.name)

        return data


class TransactionDetail(models.Model):
    """
    The base model for the classes to keep track of the transactions.
    """
    amount = models.DecimalField(decimal_places=2, max_digits=11)
    user = models.ForeignKey(User)
    transaction = models.ForeignKey(Transaction, null=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('user', 'transaction')

    def to_json(self):
        return {
            "user": self.user.username,
            "created": str(self.created),
            "amount": format_currency(self.amount),
            "type": self.__class__.__name__,
            "id": self.pk,
            # 'category': self.transaction.category.to_json()
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
