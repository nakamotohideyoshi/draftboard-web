import datetime

from django.db import models

import cash.models
from cash.exceptions import OverdraftException
from dfslog.classes import Logger, ErrorCodes
from transaction.classes import AbstractTransaction, CanDeposit
from transaction.constants import TransactionTypeConstants
from transaction.models import TransactionType


class CashTransaction(CanDeposit, AbstractTransaction):
    """
    Implements the :class:`transaction.classes.AbstractTransaction` class.
    This class handles all dealings with accounting for managing the cash
    finances.
    """

    def __init__(self, user):
        super().__init__(user)
        self.transaction_detail_class = cash.models.CashTransactionDetail
        self.balance_class = cash.models.CashBalance
        self.accountName = "cash"

    def check_sufficient_funds(self, amount):
        """
        Check to see if the user has enough funds
        :param amount: the amount to check against the user's account
        :return: True if the user has enough funds
        """
        cash_balance = self.get_balance_amount()
        #
        # allow the site to overdraft itself to allow it to keep running.
        if self.user == self.get_escrow_user() or self.user == self.get_draftboard_user():
            # TODO send email to notify of overdraft
            return True

        if (cash_balance < amount):
            return False
        return True

    def withdraw(self, amount, trans=None):
        """
        Creates a Withdraw in the user's Cash account.

        :param amount: The dollar amount that is being removed from the account.
            This should be a positive number.
        :param trans: the optional transaction to point the transaction to

        :raises :class:`cash.exceptions.OverdraftException`: When
            the user does not have enough cash for the withdrawal
        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """

        #
        # validates the amount is positive
        self.validate_amount(amount)

        #
        # Validate the user has the funds for the withdrawal
        if (not self.check_sufficient_funds(amount)):
            raise OverdraftException(self.user.username)

        #
        # creates the transaction
        category = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashWithdraw.value)
        #
        # makes the amount negative because it is a withdrawal
        self.create(category, -amount, trans)

        msg = "User[" + self.user.username + "] withdrew $" + str(
            amount) + " from their cash account."
        Logger.log(ErrorCodes.INFO, "Cash Withdraw", msg)

    def deposit(self, amount, category=None, trans=None):
        """
        Creates a Deposit in the user's Cash account.

        :param user: The user the cash is being added to.
        :param amount: The dollar amount that is being added to the account.
        :param trans: the optional transaction to point the transaction to

        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """
        #
        # validates the amount is positive
        # validates the amount is positive
        self.validate_amount(amount)

        #
        # creates the transaction
        if not category:
            category = TransactionType.objects.get(pk=TransactionTypeConstants.CashDeposit.value)
        self.create(category, amount, trans)

        msg = "User[" + self.user.username + "] deposited $" + str(
            amount) + " into their cash account."
        Logger.log(ErrorCodes.INFO, "Cash Deposit", msg)

    def deposit_gidx(self, amount, merchant_transaction_id):
        # Save a GidxTransaction that links the transaction that was just created with
        # some info for looking it up on the GIDX dashboard.
        self.deposit(amount)
        gidx_model = cash.models.GidxTransaction()
        gidx_model.merchant_transaction_id = merchant_transaction_id
        gidx_model.transaction = self.transaction_detail.transaction
        gidx_model.save()

    def withdraw_gidx(self, amount, merchant_transaction_id):
        # Save a GidxTransaction that links the transaction that was just created with
        # some info for looking it up on the GIDX dashboard.
        self.withdraw(amount)
        gidx_model = cash.models.GidxTransaction()
        gidx_model.merchant_transaction_id = merchant_transaction_id
        gidx_model.transaction = self.transaction_detail.transaction
        gidx_model.save()

    def deposit_braintree(self, amount, braintree_transaction):
        self.deposit(amount)
        braintree_model = cash.models.BraintreeTransaction()
        braintree_model.braintree_transaction = braintree_transaction
        braintree_model.transaction = self.transaction_detail.transaction
        braintree_model.save()

    def deposit_paypal_with_saved_card(self, amount, paypal_transaction_id):
        self.deposit(amount)
        saved_card_transaction = cash.models.PayPalSavedCardTransaction()
        saved_card_transaction.paypal_transaction_id = paypal_transaction_id
        saved_card_transaction.transaction = self.transaction_detail.transaction
        saved_card_transaction.save()

    def deposit_vzero(self, amount, transaction_id):
        self.deposit(amount)
        vzero_transaction = cash.models.VZeroTransaction()
        vzero_transaction.transaction_identifier = transaction_id
        vzero_transaction.transaction = self.transaction_detail.transaction
        vzero_transaction.save()

    def get_balance_string_formatted(self):
        """

        :return: the string representation of the cash balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '${:,.2f}'.format(bal)

    def get_withdrawal_count(self, past_days):
        """
        Gets the count of withdrawals for the user in the past X days.

        :param past_days: The number of days since today to get the count.
        :return: the number of withdrawals in the past X days
        """
        if past_days <= 0:
            return 0
        category = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashWithdraw.value
        )

        today = datetime.datetime.now()
        start_date = today - datetime.timedelta(days=past_days)
        return self.transaction_detail_class.objects.filter(
            created__range=[start_date, today],
            transaction__category=category
        ).count()

    def get_withdrawal_amount_current_year(self):
        """
        Gets the currents years profit for a given user.
        :return: dollars withdrawn for the year - deposits
        """
        category_withdrawal = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashWithdraw.value
        )
        category_deposit = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashDeposit.value
        )
        total_deposit = self.transaction_detail_class.objects.filter(
            created__year=datetime.datetime.now().year,
            transaction__category=category_deposit
        ).aggregate(models.Sum('amount'))
        total_withdrawal = self.transaction_detail_class.objects.filter(
            created__year=datetime.datetime.now().year,
            transaction__category=category_deposit
        ).aggregate(models.Sum('amount'))
        return abs(total_withdrawal['amount__sum'] or 0) - (total_deposit['amount__sum'] or 0)

    def get_all_deposits(self, date_range):
        """
        Gets all deposits for the user in the range of days.

        :param date_range: The range of days chosen as time period for deposit limit.
        :return: the sum of all deposits for date range
        """

        category = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashDeposit.value
        )

        return self.transaction_detail_class.objects.filter(
            created__range=date_range,
            transaction__category=category
        ).aggregate(models.Sum('amount'))
