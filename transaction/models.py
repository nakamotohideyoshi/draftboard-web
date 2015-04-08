from django.db import models

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

TRANSACTION_CATEGORY = (
	('contest-buyin', 		'Contest Buyin'),
	('contest-payout', 		'Contest Payout'),
	('funds-deposit', 		'Funds Deposit'),
	('funds-withdrawal', 	'Funds Withdrawal'),
	# ('xxx', 'Xxx'),
	# ('xxx', 'Xxx'),
	# ('xxx', 'Xxx'),
)

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


class TransactionDetail( models.Model ):
    """
    The base model for the classes to keep track of
    the transactions.
    """
    amount      = models.DecimalField(decimal_places=2, max_digits=7)
    user        = models.ForeignKey( User )
    transaction = models.ForeignKey( Transaction )
    created  = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        abstract = True
        unique_together = ('user', 'transaction')



class Balance( models.Model ):

    """
    The base model for classes to maintain a balance based
    off the TransactionDetail.

    """
    user 				= models.OneToOneField( User, primary_key=True  )
    amount 				= models.DecimalField(decimal_places=2, max_digits=7)

    #
    # The foreign key to the Transaction Detail type
    transaction_type = models.ForeignKey(ContentType, null=True)
    transaction_id = models.PositiveIntegerField(null = True)
    transaction = GenericForeignKey('transaction_type', 'transaction_id')
    updated  = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True



