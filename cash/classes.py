#from cash.models import CashBalance, CashTransactionDetail
import cash.models
from transaction.classes import AbstractTransaction
from transaction.models import TransactionType
from transaction.constants import TransactionTypeConstants
from cash.exceptions import OverdraftException, IncorrectVariableTypeException
from dfslog.classes import Logger, ErrorCodes
from django.contrib.auth.models import User
from django.conf import settings
from django.db import models

import datetime
class CashTransaction(AbstractTransaction):
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
        if(cash_balance < amount):
            return False
        return True


    def withdraw(self, amount):
        """
        Creates a Withdraw in the user's Cash account.

        :param amount: The dollar amount that is being removed from the account.
            This should be a positive number.

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
        if(not self.check_sufficient_funds( amount)):
            raise OverdraftException(self.user.username)

        #
        #creates the transaction
        category = TransactionType.objects.get(pk=TransactionTypeConstants.CashWithdrawal.value)
        #
        # makes the amount negative because it is a withdrawal
        self.create(category,-amount)
        Logger.log(ErrorCodes.INFO,"Withdrawal", self.user.username+" withdrew $"+str(amount)+" from their cash account.")


    def deposit(self, amount):
        """
        Creates a Deposit in the user's Cash account.

        :param user: The user the cash is being added to.
        :param amount: The dollar amount that is being added to the account.

        :raises :class:`transaction.exceptions.AmountNegativeException`:
            When the amount is a negative number.
        """
        #
        # validates the amount is positive
        # validates the amount is positive
        self.validate_amount(amount)

        #
        #creates the transaction
        category = TransactionType.objects.get(pk=TransactionTypeConstants.CashDeposit.value)
        self.create(category,amount)
        Logger.log(ErrorCodes.INFO, "Deposit", self.user.username+" deposited $"+str(amount)+" into their cash account.")


    def deposit_braintree(self, amount, braintree_transaction):
        self.deposit(amount)
        braintree_model = cash.models.BraintreeTransaction()
        braintree_model.braintree_transaction = braintree_transaction
        braintree_model.transaction = self.transaction_detail.transaction
        braintree_model.save()



    def get_balance_string_formatted(self):
        """

        :return: the string representation of the cash balance
            i.e. $5.50

        """
        bal = self.get_balance_amount()
        return '${:,.2f}'.format(bal)

    def get_withdrawal_count(self, past_days ):
        """
        Gets the count of withdrawals for the user in the past X days.

        :param past_days: The number of days since today to get the count.
        :return: the number of withdrawals in the past X days
        """
        if(past_days <=0):
            return 0
        category = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashWithdrawal.value
        )

        today = datetime.today()
        end_date = today + datetime.timedelta(days=past_days)
        return self.transaction_detail_class.objects.count(
            created__range=[today, end_date],
            category = category
        )

    def get_withdrawal_amount_current_year(self ):
        """
        Gets the currents years profit for a given user.
        :return:dollars withdrawn for the year - deposits
        """
        category_withdrawal = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashWithdrawal.value
        )
        category_deposit = TransactionType.objects.get(
            pk=TransactionTypeConstants.CashDeposit.value
        )
        total_deposit = self.transaction_detail_class.objects.filter(
            created__year=datetime.now().year,
            category = category_deposit
        ).aggregate(models.Sum('amount'))
        total_withdrawal = self.transaction_detail_class.objects.filter(
            created__year=datetime.now().year,
            category = category_deposit
        ).aggregate(models.Sum('amount'))

        return abs(total_withdrawal) - total_deposit

#-------------------------------------------------------------------
#-------------------------------------------------------------------
class CashWithdrawalManager:

    def __init__(self, user):
        if(not isinstance(user, User)):
            raise IncorrectVariableTypeException(
                    type(self).__name__,
                    "user"
            )

        self.user = user



    def withdraw(self, amount, paypal_email= None):

        #
        # Remove the cash from the users account
        ct = CashTransaction(self.user)
        ct.withdraw(amount)


        withdrawal_status = cash.models.WithdrawalStatus()


        #
        # Gets the user's  amount of withdrawal requests for the
        # past day, week, and month
        past_day_withdrawal_count = ct.get_withdrawal_count(1)
        past_week_withdrawal_count = ct.get_withdrawal_count(7)
        past_month_withdrawal_count = ct.get_withdrawal_count(30)

        #
        # Compares the counts to the withdrawal rules in the
        # app settings. If they are greater than or equal
        # to the limits the withdrawal will be flagged for
        # admin approval.
        if(past_day_withdrawal_count >=
                settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_DAILY_FREQ or
           past_week_withdrawal_count >=
                settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_WEEKLY_FREQ or
           past_month_withdrawal_count >=
                settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_MONTHLY_FREQ or
           amount >=
                settings.DFS_CASH_WITHDRAWAL_APPROVAL_REQ_AMOUNT
           ):
            withdrawal_status.flagged = True


        #
        # Gets the profit for the year + the amount requested by the user
        current_year_profit = ct.get_withdrawal_amount_current_year() + amount

        #
        # If they have profited enough for the site to have to
        # provide tax documentation.
        if(current_year_profit >
            settings.DFS_CASH_WITHDRAWAL_AMOUNT_REQUEST_TAX_INFO):

            #
            # Check to see if we have collected the tax information
            # for the given user. If not flag them and set tax_info_required
            tax_info_manager = TaxInfoManager(self.user)
            if(not tax_info_manager.info_collected()):
                withdrawal_status.flagged = True
                withdrawal_status.tax_info_required = True

        #
        # If nothing has been flagged as an issue and PayPal was set,
        # it means we can try to automatically pay them out.
        if(paypal_email != None and withdrawal_status.flagged == False):
            withdrawal_status.paypal_email = paypal_email
            withdrawal_status.approved = self.__payout_paypal(
                                            amount,
                                            paypal_email
                                        )


        # Otherwise the admin needs to write the check or approve the
        # PayPal payout.
        else:
            withdrawal_status.mail_check = True
            withdrawal_status.paypal_email = ''

        #
        # link the withdrawal status to the transaction_detail
        # from the newly withdrawn cash transaction
        withdrawal_status.cash_transaction_detail = ct.transaction_detail
        withdrawal_status.save()





    def __payout_paypal(self, amount, paypal_email):
        """
        TODO still

        Pays out via PayPal an amount to the user
        :param amount: amount to pay PayPal
        :param paypal_email: the User's email address
        :return: if successful
        """
        return True


#-------------------------------------------------------------------
#-------------------------------------------------------------------
class TaxInfoManager:
    def __init__(self, user):
        if(not isinstance(user, User)):
            raise IncorrectVariableTypeException(
                    type(self).__name__,
                    "user"
            )

        self.user = user

    def info_collected(self):
        """
        TODO
        :return: whether the information for taxes has been collected
        """
        return True

























