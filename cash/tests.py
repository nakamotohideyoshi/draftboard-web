import unittest
import decimal
from django.contrib.auth.models import User
from cash.classes import CashTransaction
from cash.models import CashBalance, CashTransactionDetail
from transaction.exceptions import IncorrectVariableTypeException
class CashTransactionTest(unittest.TestCase):
    """
    Tests the :class:`cash.classes.CashTransaction` class
    """
    def test(self):
        """
        Test the additional functionality of Cash Transaction that was
        not implemented in the :class:`transaction.classes.Transaction` class.
        """
        USERNAME = 'test_user'
        AMOUNT= decimal.Decimal(5.24)
        AMOUNT_2 = decimal.Decimal(5.38)
        AMOUNT_3_NEGATIVE = decimal.Decimal(3.33)
        AMOUNT_4 = decimal.Decimal(100.00)
        try:
            user = User.objects.get(username = USERNAME)
        except User.DoesNotExist:
            user = User.objects.create(username=USERNAME)
            user.save()



        def create_deposit(user, amount, balance_result):
            test = CashTransaction(user)
            test.deposit(amount)
            tran_det= CashTransactionDetail.objects.get(
                        user=test.transaction_detail.user,
                        transaction=test.transaction_detail.transaction)
            self.assertAlmostEquals(tran_det.amount, amount)
            bal = CashBalance.objects.get(
                user=test.transaction_detail.user)
            self.assertAlmostEquals(bal.amount,balance_result)
            self.assertEquals(bal.transaction, tran_det)

        def create_withdrawal(user, amount, balance_result):
            test = CashTransaction(user)
            test.withdraw(amount)
            tran_det= CashTransactionDetail.objects.get(
                        user=test.transaction_detail.user,
                        transaction=test.transaction_detail.transaction)
            self.assertAlmostEquals(tran_det.amount, -amount)
            bal = CashBalance.objects.get(
                user=test.transaction_detail.user)
            self.assertAlmostEquals(bal.amount,balance_result)
            self.assertEquals(bal.transaction, tran_det)

        #
        # Tests deposit
        create_deposit(user, AMOUNT, AMOUNT )


        #
        # Tests second deposit and balance
        create_deposit(user, AMOUNT_2, AMOUNT + AMOUNT_2)



        #
        # Tests that balance gets updated when there is a creation
        # of an additional NEGATIVE transaction_detail
        create_withdrawal(user, AMOUNT_3_NEGATIVE, AMOUNT + AMOUNT_2 - AMOUNT_3_NEGATIVE)



        #
        # Test with multiple transactions and no existence of a balance
        CashBalance.objects.get(user=user).delete()
        create_deposit(user, AMOUNT_4, (AMOUNT + AMOUNT_2 - AMOUNT_3_NEGATIVE+ AMOUNT_4))

        #
        # Tests creation of object with an object that is not a user
        self.assertRaises(IncorrectVariableTypeException, lambda: CashTransaction(1))