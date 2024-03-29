import fpp.models

from django.utils import timezone
from datetime import timedelta
from transaction.constants import TransactionTypeConstants
from transaction.classes import AbstractTransaction
from transaction.models import TransactionType
from .exceptions import WithdrawRakepaidException
from .models import RakepaidBalance, RakepaidTransactionDetail
from .models import LoyaltyStatus, PlayerTier
from django.db.models import Sum
from dfslog.classes import Logger, ErrorCodes

class LoyaltyStatusManager(object):
    BASE_LOYALTY_MULTIPLIER = 10.0 # RAKE MULTIPLIER TO FPP
    #
    # used by a migration to install the initial loyalty statuses
    DEFAULT_STATUSES = [
        {
            'name'              : 'Bronze',
            'rank'              : 1,
            'thirty_day_avg'    : 0.0,
            'multiplier'        : 1.0
        },
        {
            'name'              : 'Silver',
            'rank'              : 2,
            'thirty_day_avg'    : 10.0,
            'multiplier'        : 2.0
        },
        {
            'name'              : 'Gold',
            'rank'              : 3,
            'thirty_day_avg'    : 100.0,
            'multiplier'        : 3.0
        }
    ]

    def __init__(self, user):
        self.user                   = user
        try:
            self.player_tier = PlayerTier.objects.get(user=self.user)
        except PlayerTier.DoesNotExist:
            self.player_tier = PlayerTier()
            self.player_tier.user   = self.user
            self.player_tier.status = LoyaltyStatus.objects.get( rank=1 ) # start at the lowest status
            self.player_tier.save()

    def update(self):
        """
        based on the last 30 days, update this users LoyaltyStatus
        """

        thirty_days_ago = timezone.now() - timedelta(days=30)
        rake_agg = RakepaidTransactionDetail.objects.filter( created__gte=thirty_days_ago,
                                                  user=self.user ).aggregate(Sum('amount'))

        #
        # all the rakepaid transactions times a 1.0 multiplier are considered the
        # "base" fpp really -- from a calculation standpoint, that is.
        total = rake_agg.get('amount__sum')  # will return None if its 0 !
        if total is None:
            total = 0.0

        #
        # figure out which loyalty tier this total puts this user into, and apply it
        statuses        = LoyaltyStatus.objects.filter(thirty_day_avg__gte=total).order_by('rank')  # sort ascending
        highest_tier    = statuses[ len(statuses) - 1 ]                 # highest status
        new_tier        = list(statuses[:1])[0]                         # the first item in the sorted list

        if not new_tier:
            new_tier = highest_tier

        #
        # at this point, simply set the new_tier, but only if it differs from
        # what is already set, because theres no point in calling save() otherwise!
        if self.player_tier.status != new_tier:
            self.player_tier.status = new_tier
            self.player_tier.save()

    def get_fpp_multiplier(self):
        """
        Return the users current FPP multiplier.
        """
        return self.player_tier.status.multiplier

class RakepaidTransaction(AbstractTransaction):
    """
    Implements the :class:`transaction.classes.AbstractTransaction` class.
    This class handles all dealings with accounting for managing the rake paid
    of the user
    """
    def __init__(self, user):
        super().__init__(user)
        self.transaction_detail_class = RakepaidTransactionDetail
        self.balance_class = RakepaidBalance
        self.accountName = "rakepaid"

    def check_sufficient_funds(self, amount):
        """
        Check to see if the user has at least this amount
        :param amount: the amount to check against the user's account
        :return: True if the user has the amount available
        """
        balance = self.get_balance_amount()
        if(balance < amount):
            return False
        return True

    def withdraw(self, amount, trans=None):
        """
        throws an exception if called. You should not be able to withdraw
        from the Rakepaid table
        :raises:
        """
        raise WithdrawRakepaidException()

    def deposit(self, amount, category=None, trans=None):
        """
        Creates a Deposit in the users FPP account

        :param user: The user the amount is being added to.
        :param amount: The amount being added to the account.
        :param trans: the optional transaction to point the transaction to


        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        # validates the amount is positive
        self.validate_amount(amount)

        #
        # creates the transaction
        if(category == None):
            category = TransactionType.objects.get(pk=TransactionTypeConstants.CashDeposit.value)
        self.create(category,amount, trans)
        Logger.log(ErrorCodes.INFO, "Rakepaid Deposit", self.user.username+" deposited $"+str(amount)+" into their account.")

    def get_balance_string_formatted(self):
        """

        :return: the string representation of the fpp balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '{:,.0f} FPP'.format(bal)

