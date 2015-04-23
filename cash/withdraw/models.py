from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save

from mysite.legal import state_choices          # list of tuples, ie: [('NH','NH'), ..., ]

from cash.models import CashTransactionDetail

import datetime

class WithdrawStatus( models.Model ):
    """
    The class that keeps a list of all the statuses
    their corresponding string representation.
    """
    category    = models.CharField(max_length=100, null=False)
    name        = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return '%s  %s' % (self.category, self.name)

class Withdraw(models.Model):
    """
    Abstract implementation fo the withdraw
    """
    created                 = models.DateTimeField(auto_now_add=True, null=True)
    cash_transaction_detail = models.OneToOneField( CashTransactionDetail , null=False )
    status                  = models.ForeignKey( WithdrawStatus, null=False )
    status_updated          = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    #
    # inheriting classes MUST override this method, because it will be used
    # in the admin panel where user's requests to withdraw money are displayed.
    def __str__(self):
        raise Exception( self.__class__.__name__ + ' must be overridden in child class!' )

    @property
    def age(self):
        now = datetime.datetime.now()
        return '%s' % (now - self.created)   # ie: 2 days, hh:mm:ss

class PayPalWithdraw(Withdraw):
    email               = models.EmailField(null=False)
    paypal_transaction  = models.CharField( max_length=255, null=False )

    def __str__(self):
        return '%s paypal-account-email[  %s  ]' % (self.__class__.__name__, self.email)

class CheckWithdraw(Withdraw):

    check_number    = models.IntegerField(null=True, unique=True )
    fullname        = models.CharField(max_length=100, null=False, default='')
    address1        = models.CharField(max_length=255, null=False, default='')
    address2        = models.CharField(max_length=255, null=False, default='')
    city            = models.CharField(max_length=64, null=False, default='')
    state           = models.CharField(choices=state_choices, max_length=2,  default='')
    zipcode         = models.CharField(max_length=5, null=False, default='')

    @property
    def address(self):
        return '%s\n %s %s\n %s, %s %s' % (self.fullname, self.address1,
                                           self.address2, self.city, self.state, self.zipcode)

    def __str__(self):
        return '%s check-number[  %s  ]  mailing-address[  %s  ]' % (self.__class__.__name__, str(self.check_number), self.address )

class ReviewPendingWithdraw(models.Model):
    """
    this will point to a Withdraw model and we'll be able to display them in one table

    this model is AUTOMATICALLY created, so long as you have connected your model
    ie: post_save.connect( create_from_signal, sender=YourModelWithdraw )

    you can access the basic properties of the base Withdraw class because of the @property tagged methods
    """

    content_type    = models.ForeignKey( ContentType )
    object_id       = models.PositiveIntegerField()
    content_object  = generic.GenericForeignKey( 'content_type', 'object_id' )

    #
    # this is the method that listens for PayPayl, Check withdraws and creates itself
    def create_from_signal(sender, **kwargs):
        if 'created' in kwargs and kwargs['created']:
            instance = kwargs['instance']
            ctype = ContentType.objects.get_for_model( instance )
            pending_withdraw = ReviewPendingWithdraw.objects.get_or_create(content_type=ctype,
                                                                           object_id=instance.id )
    #
    # register this RewviewPendingWithdraw to create a new one when these models are created
    post_save.connect( create_from_signal, sender=PayPalWithdraw )
    post_save.connect( create_from_signal, sender=CheckWithdraw )

    @property
    def withdraw(self):
        the_model = self.content_type.model_class()
        return the_model.objects.get( pk=self.object_id )

    @property
    def created(self):
        return self.content_object.created

    @property
    def user(self):
        return self.content_object.cash_transaction_detail.user

    @property
    def cash_transaction_detail(self):
        return self.content_object.cash_transaction_detail

    @property
    def status(self):
        return self.content_object.status.name
