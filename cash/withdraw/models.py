from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save
from mysite.legal import STATE_CHOICES          # list of tuples, ie: [('NH','NH'), ..., ]
from cash.models import CashTransactionDetail
from django.contrib.postgres.fields import JSONField


class WithdrawStatus(models.Model):
    """
    The class that keeps a list of all the statuses
    their corresponding string representation.
    """
    category = models.CharField(max_length=100, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=255, null=False)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return '%s' % (self.category)


class Withdraw(models.Model):
    """
    Abstract implementation fo the withdraw
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    cash_transaction_detail = models.OneToOneField(CashTransactionDetail, null=False)
    status = models.ForeignKey(WithdrawStatus, null=False)
    status_updated = models.DateTimeField(auto_now=True,
                                          verbose_name='NetProfit @ Withdraw Time')
    net_profit = models.DecimalField(decimal_places=2, max_digits=7,
                                     verbose_name='NetProfit @ Withdraw Time')
    processed_at = models.DateTimeField(null=True,
                                        verbose_name='Proccessed At')

    class Meta:
        abstract = True

    #
    # inheriting classes MUST override this method, because it will be used
    # in the admin panel where user's requests to withdraw money are displayed.
    def __str__(self):
        raise Exception(self.__class__.__name__ + ' must be overridden in child class!')

    # note: there is a template tag called 'timesince' & 'timeuntil' , just fyi

    @property
    def user(self):
        return self.cash_transaction_detail.user

    @property
    def username(self):
        return self.cash_transaction_detail.user.username

    @property
    def amount(self):
        return self.cash_transaction_detail.amount


class PayPalWithdraw(Withdraw):
    email = models.EmailField(null=False)

    paypal_payout_item = models.CharField(max_length=255, null=False, default='',
                                          verbose_name='PayPal Payout Item ID')
    paypal_transaction = models.CharField(max_length=255, null=False, default='',
                                          verbose_name='PayPal Transaction ID')
    paypal_transaction_status = models.CharField(max_length=255, null=False, default='',
                                                 verbose_name='PayPal Transaction Status')

    started_processing = models.DateTimeField(null=True)
    paypal_errors = models.CharField(max_length=2048, default='')

    def __str__(self):
        return '%s paypal-account-email[  %s  ]' % (self.__class__.__name__, self.email)


class CheckWithdraw(Withdraw):

    check_number = models.IntegerField(null=True, unique=True, blank=True)
    fullname = models.CharField(max_length=100, null=False, default='')
    address1 = models.CharField(max_length=255, null=False, default='')
    address2 = models.CharField(max_length=255, null=False, default='')
    city = models.CharField(max_length=64, null=False, default='')
    state = models.CharField(choices=STATE_CHOICES, max_length=2,  default='')
    zipcode = models.CharField(max_length=5, null=False, default='')

    @property
    def address(self):
        return '%s\n %s %s\n %s, %s %s' % (self.fullname, self.address1,
                                           self.address2, self.city, self.state, self.zipcode)

    def __str__(self):
        return '%s check-number[  %s  ]  mailing-address[  %s  ]' % (
                self.__class__.__name__, str(self.check_number), self.address)


class ReviewPendingWithdraw(models.Model):
    """
    this will point to a Withdraw model and we'll be able to display them in one table

    this model is AUTOMATICALLY created, so long as you have connected your model
    ie: post_save.connect( create_from_signal, sender=YourModelWithdraw )

    you can access the basic properties of the base Withdraw class because of the @property tagged
    methods
    """

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    #
    # this is the method that listens for PayPayl, Check withdraws and creates itself
    def create_from_signal(sender, **kwargs):
        if 'created' in kwargs and kwargs['created']:
            instance = kwargs['instance']
            ctype = ContentType.objects.get_for_model(instance)
            pending_withdraw = ReviewPendingWithdraw.objects.get_or_create(content_type=ctype,
                                                                           object_id=instance.id)
    #
    # register this RewviewPendingWithdraw to create a new one when these models are created
    post_save.connect(create_from_signal, sender=PayPalWithdraw)
    post_save.connect(create_from_signal, sender=CheckWithdraw)

    @property
    def withdraw(self):
        the_model = self.content_type.model_class()
        return the_model.objects.get(pk=self.object_id)

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


class AutomaticWithdraw(models.Model):
    """
    a model for the cutoff where we will automatically process a withdraw (cashout)
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    auto_payout_below = models.DecimalField(decimal_places=2, max_digits=9)


class PendingWithdrawMax(models.Model):
    """
    a model for the cutoff where we will automatically process a withdraw (cashout)
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    max_pending = models.IntegerField(default=3, null=False)


class CashoutWithdrawSetting(models.Model):
    """
    holds the min and max dollar amounts for individual cashout requests
    """
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    max_withdraw_amount = models.DecimalField(decimal_places=2, max_digits=9, default=10000.00)
    min_withdraw_amount = models.DecimalField(decimal_places=2, max_digits=9, default=5.00)


class PayoutTransaction(models.Model):
    """
    every response from having tried to process a paypal payout
    """

    created = models.DateTimeField(auto_now_add=True)

    data = JSONField()

    withdraw_type = models.ForeignKey(ContentType)
    withdraw_id = models.PositiveIntegerField()
    withdraw = GenericForeignKey('withdraw_type', 'withdraw_id')

    class Meta:
        get_latest_by = 'created'
