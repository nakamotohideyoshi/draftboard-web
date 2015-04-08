import unittest
from transaction.classes import AbstractTransaction
from django.contrib.auth.models import User
from transaction.models import TransactionDetail, Balance, TransactionType
from transaction.exceptions import VariableNotSetException, IncorrectVariableTypeException, AmountNegativeException
import decimal
from django.core.exceptions import ValidationError
from test.models import TransactionDetailChild, BalanceChild


class AbstractTransactionTest(unittest.TestCase):
    """
    Tests the :class:`transaction.classes.AbstractTransaction` class
    """

    def test_transaction_system(self):
        """
        Tests to verify the exceptions are thrown when the child
        class is implemented improperly.
        """
        class TransactionChild(AbstractTransaction):
            def __init__(self, user):
                super().__init__(user)
                self.transaction_detail_class = TransactionDetailChild
                self.balance_class = BalanceChild
                self.accountName = "test"


        USERNAME = 'test_user'
        TRANSACTION_TYPE_CATEGORY = 'test_cat'
        TRANSACTION_TYPE_NAME = 'transaction_type_name'
        TRANSACTION_TYPE_DES = 'transaction_type_desc'
        AMOUNT = decimal.Decimal(5.24)
        AMOUNT_2 = decimal.Decimal(5.38)
        AMOUNT_3_NEGATIVE = decimal.Decimal(-3.33)
        AMOUNT_4 = decimal.Decimal(100.00)
        try:
            user = User.objects.get(username = USERNAME)
        except User.DoesNotExist:
            user = User.objects.create(username=USERNAME)
            user.save()

        category = TransactionType(category=TRANSACTION_TYPE_CATEGORY,
                                   name= TRANSACTION_TYPE_NAME,
                                   description = TRANSACTION_TYPE_DES)
        category.save()

        def create_transaction( user, category, amount, balance_result):
            #
            # Tests that balance gets updated when there is a creation
            # of an additional NEGATIVE transaction_detail
            test = TransactionChild(user)
            test.create( category, amount)
            tran_det= TransactionDetailChild.objects.get(
                        user=test.transaction_detail.user,
                        transaction=test.transaction_detail.transaction)
            self.assertAlmostEquals(tran_det.amount, amount)
            bal = BalanceChild.objects.get(
                user=test.transaction_detail.user)
            self.assertAlmostEquals(bal.amount,balance_result)
            self.assertEquals(bal.transaction, tran_det)

        #
        # Tests a child class that does not set the local variables
        class NotImplementedTranasactionChild(AbstractTransaction):
            def __init__(self, user):
                super().__init__(user)
        test = NotImplementedTranasactionChild(user)
        self.assertRaises(VariableNotSetException, lambda: test.create(1,1))

        #
        # Tests with a working class.
        create_transaction(user, category, AMOUNT, AMOUNT )


        #
        # Tests the create method with improper arguments
        test = TransactionChild(user)
        self.assertRaises(IncorrectVariableTypeException, lambda:test.create( 1, AMOUNT))
        self.assertRaises(ValidationError, lambda:test.create( category, "bad"))
        #
        # Tests teh validate amount record to make sure it only accepts positive integers
        self.assertRaises(AmountNegativeException, lambda:test.validate_amount(-0.01))


        #
        # Tests that balance gets updated when there is a creation
        # of an additional transaction_detail
        create_transaction(user, category, AMOUNT_2, AMOUNT + AMOUNT_2)



        #
        # Tests that balance gets updated when there is a creation
        # of an additional NEGATIVE transaction_detail
        create_transaction(user, category, AMOUNT_3_NEGATIVE, AMOUNT + AMOUNT_2 + AMOUNT_3_NEGATIVE)



        #
        # Test with multiple transactions and no existance of a balance
        BalanceChild.objects.get(user=user).delete()
        create_transaction(user, category, AMOUNT_4, (AMOUNT + AMOUNT_2 + AMOUNT_3_NEGATIVE+ AMOUNT_4))

        #
        # Tests creation of object with an object that is not a user
        self.assertRaises(IncorrectVariableTypeException, lambda: TransactionChild(1))

