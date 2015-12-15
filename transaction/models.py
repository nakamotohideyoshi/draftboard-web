from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db.models.deletion import Collector

TRANSACTION_CATEGORY = (
	('contest-buyin', 		'Contest Buyin'),
	('contest-payout', 		'Contest Payout'),
	('funds-deposit', 		'Funds Deposit'),
	('funds-withdrawal', 	'Funds Withdrawal'),
	# ('xxx', 'Xxx'),
	# ('xxx', 'Xxx'),
	# ('xxx', 'Xxx'),
)

class AbstractAmount(models.Model):

    def get_category(self):
        # should return "CashAmount", or "TicketAmount", etc...
        raise Exception('inheriting class must implement this method: transaction.models.AbstractAmount.get_amount_type()')

    def get_transaction_class(self):
        raise Exception('inheriting class must implement this method: transaction.models.AbstractAmount.get_transaction_class()')

    def get_cash_value(self):
        raise Exception('inheriting class must implement this method: transaction.models.AbstractAmount.get_cash_value()')

    class Meta:
        abstract = True

class TransactionType( models.Model ):
    """
    The class that keeps a list of all the transaction
    types/actions and their corresponding string representation.
    """
    category    = models.CharField(max_length=100, null=False)
    name        = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return '%s  %s' % (self.category, self.name)

class Transaction( models.Model ):
    """
    This class keeps track of all
    """
    category = models.ForeignKey( TransactionType )
    user 	 = models.ForeignKey( User )
    created  = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return '%s  %s  %s' % (self.created.date(), self.user, self.category)

    def to_json(self):
        collector = Collector(using='default') # or specific database
        collector.collect([self])
        array = []
        for model_tmp, instance_tmp in collector.instances_with_model():
            print("HERE "+str(instance_tmp))
            if hasattr(instance_tmp, "to_json") and instance_tmp != self and instance_tmp.user == self.user:
                array.append(instance_tmp.to_json())

        return {"created":str(self.created), "details":array, "id":self.pk}

class TransactionDetail( models.Model ):
    """
    The base model for the classes to keep track of
    the transactions.
    """
    amount      = models.DecimalField(decimal_places=2, max_digits=11)
    user        = models.ForeignKey( User )
    transaction = models.ForeignKey( Transaction, null=False, related_name='+')
    created  = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('user', 'transaction')


    def to_json(self):
        return {"created":str(self.created), "amount":self.amount, "type": self.__class__.__name__ , "id":self.pk}

class Balance( models.Model ):

    """
    The base model for classes to maintain a balance based
    off the TransactionDetail.

    """
    user 				= models.OneToOneField( User, primary_key=True  )
    amount 				= models.DecimalField(decimal_places=2, max_digits=11)
    updated  = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

