#
# cash/tests/tests.py

import decimal
from django.contrib.auth.models import User
from cash.classes import CashTransaction
from cash.models import CashBalance, CashTransactionDetail
from mysite.exceptions import IncorrectVariableTypeException
from cash.models import AdminCashDeposit, AdminCashWithdrawal, BraintreeTransaction
from test.classes import AbstractTest
from django.test.client import Client
from django.contrib.auth.models import Permission
from django.utils.crypto import get_random_string

class InitialCashTransactionTest(AbstractTest):
    """
    ensures the first transaction creates the balance entry if necessary
    """
    def setUp(self):
        super().setUp()
        self.user       = self.get_user('testuser')
        self.amount     = decimal.Decimal(10.00)

    def test_create_first_deposit(self):
        ct = CashTransaction(self.user)
        ct.deposit( self.amount )
        self.assertAlmostEquals( ct.get_balance_amount(), self.amount )

class CashTransactionTest(AbstractTest):
    """
    Tests the :class:`cash.classes.CashTransaction` class
    """
    def setUp(self):
        super().setUp()
        self.USERNAME   = 'test_user'
        self.user       = self.get_user(self.USERNAME)

        self.AMOUNT             = decimal.Decimal(5.24)
        self.AMOUNT_2           = decimal.Decimal(5.38)
        self.AMOUNT_3_NEGATIVE  = decimal.Decimal(3.33)
        self.AMOUNT_4           = decimal.Decimal(100.00)

    def test(self):
        """
        Test the additional functionality of Cash Transaction that was
        not implemented in the :class:`transaction.classes.Transaction` class.
        """
        # USERNAME = 'test_user'
        # AMOUNT= decimal.Decimal(5.24)
        # AMOUNT_2 = decimal.Decimal(5.38)
        # AMOUNT_3_NEGATIVE = decimal.Decimal(3.33)
        # AMOUNT_4 = decimal.Decimal(100.00)
        # user = self.get_user(USERNAME)

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
            #self.assertEquals(bal.transaction, tran_det)

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
            #self.assertEquals(bal.transaction, tran_det)

        #
        # Tests deposit
        running_total = self.AMOUNT
        create_deposit(self.user, self.AMOUNT, running_total )

        #
        # Tests second deposit and balance
        running_total += self.AMOUNT_2
        create_deposit(self.user, self.AMOUNT_2, running_total)

        #
        # Tests that balance gets updated when there is a creation
        # of an additional NEGATIVE transaction_detail
        running_total -= self.AMOUNT_3_NEGATIVE
        create_withdrawal(self.user, self.AMOUNT_3_NEGATIVE, running_total)

        #
        # # if you delete the balance while there are transactions,
        # # the balance will start over at 0.00, although
        # # you would be able to recalculate the actual balance
        # # using the historical user transactions. the balance is just a counter
        # # Test with multiple transactions and no existence of a balance
        # running_total += self.AMOUNT_4
        # CashBalance.objects.get(user=self.user).delete()
        # create_deposit(self.user, self.AMOUNT_4, running_total)

        #
        # Tests creation of object with an object that is not a user
        self.assertRaises(IncorrectVariableTypeException, lambda: CashTransaction(1))

# class DepositViewTest(AbstractTest): # im not sure its possible, because of the way braintree form works
#     """
#     test the functionality of adding funds to the site using braintree.
#
#     TODOs
#         - Amount Field
#             -No amount
#             -Improper value
#             -Max amount
#             -Min amount
#         - payment_method_nonce
#             - missing
#             - incorrect
#         - Test being logged out
#     """
#
#     def setUp(self):
#         self.admin          = self.get_admin_user()
#         self.url_submit     = '/api/cash/deposit/'
#         self.url_success    = DepositView.success_redirect_url
#         self.url_fail       = DepositView.failure_redirect_url
#
#         client = Client()
#         client.login( username=self.admin.username, password=self.get_password() )
#         self.client = client
#
#     def __post(self, val):
#         form_data = {
#             'user'      : self.admin.pk,
#             'amount'    : val, # dont cast it - in case we're trying to test something tricky
#             'reason'    : 'testing...'
#         }
#         response = self.client.post( self.url_submit )
#         self.assertIsNotNone( response )
#         return response
#
#     def test_deposit_zero_amount(self):
#         AMOUNT = 0.0
#         response = self.__post( AMOUNT )
#         self.assertEquals( response.status_code, 200 )
#
#         #braintree_deposits = BraintreeTransaction.objects.all()
#         #self.assertEquals(len(braintree_deposits), 1)
#
#     # def test_deposit_negative_value(self):
#     #     AMOUNT = -0.0
#     #     response = self.__post( AMOUNT )
#     #
#     # def test_deposit_non_numeric_value(self):
#     #     AMOUNT = 'abc'
#     #     response = self.__post( AMOUNT )




# class BraintreeDeposit(AbstractTest):
#     """
#     test the CashTransaction.braintree_deposit() method.
#
#     creates random braintree_transaction_ids for testing purposes!
#     (ie: you cant look them up in the braintree account)
#
#     """
#     def setUp(self):
#         self.admin     = self.get_admin_user()
#         self.ct         = CashTransaction( self.admin )
#
#     def __braintree_transaction_deposit(self, amount):
#         # count the braintree transactions before we create the new one
#         count_btree_trans_before = len( BraintreeTransaction.objects.all() )
#
#         # generate a fake id
#         braintree_transaction_id = get_random_string( 8 )
#         self.ct.deposit_braintree( amount, braintree_transaction_id )
#
#         count_btree_trans_after = len( BraintreeTransaction.objects.all() )
#
#         self.assertEquals(count_btree_trans_before + 1, count_btree_trans_after)



class BalanceAPIViewTest(AbstractTest):
    """
    TODOs
        -Balance of user with no balance
        -Validate format of the json
    """
    pass

class TransactionHistoryAPIViewTest(AbstractTest):
    """
    TODOs
        -Test dates
    """
    pass



class AdminPanelCashDeposit(AbstractTest):
    """
    Test the AdminCashDepositForm for validity

    """

    c       = Client()
    url     = '/thinking_face/cash/admincashdeposit/add/'
    user_data = {
        'username'      : 'admin',      # subclasses should set the username here
        'password'      : 'password',      # subclasses should set the password here
        'is_superuser'  : True,
        'is_staff'      : True,
        'permissions'   : []            # superusers will have all permissions regardless of this list
    }
    amount = 1.00

    def setUp(self):
        super().setUp()
        # nothing much to do here

    def __user_exists(self, username):
        try:
            u = User.objects.get( username=username )
            return True
        except User.DoesNotExist:
            return False

    def __get_or_create_user_with_perm(self, username='', password='',
                                       is_superuser=False, is_staff=False, permissions=[]):
        #
        # get the user if they exist.
        # if they dont exist, create them with the specified status and permissions
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            if is_superuser:
                # superuser, by default is also staff
                user.is_superuser   = True
                user.is_staff       = True
            elif is_staff == True and is_superuser == False:
                # staff , but not super user
                user.is_superuser = False
                user.is_staff = True

                # if there are specified permissions, apply them to the staff
                for perm in permissions:
                    user.user_permissions.add( perm )

            else:
                # basic user
                user.is_superuser = False
                user.is_staff   = False

            user.save()
        return user

    def test_admin_add_cash_deposit_view(self):

        admin = self.get_admin_user()

        users = User.objects.all()
        print('users: ', str(len(users)))
        for u in users:
            print( u )

        self.assertEquals( admin.username, 'admin')


        self.assertEquals( self.c.login( username=admin.username,
                                    password=self.get_password() ), True )

        # confirm again the person we think is logged in really is:
        logged_in_user_id = None
        for tup in self.c.session.items():
            if tup[0] == '_auth_user_id':
                logged_in_user_id = tup[1]
        self.assertEquals( logged_in_user_id, '%s' % str(admin.pk) )

        form_data = {
            'user'      : admin.pk,          # set later on when the user is created
            'amount'    : self.amount,
            'reason'    : 'testing-%s' % self.__class__.__name__
        }
        #form_data['user'] = admin.pk

        try:
            response = self.c.post( self.url, form_data )
        except AttributeError:
            pass

        #
        # check if there are ANY new AdminCashDeposits in the database
        acds = AdminCashDeposit.objects.all()
        print('%s - total AdminCashDeposit objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        acd = AdminCashDeposit.objects.get ( user=admin, reason=form_data['reason'] )
        print( acd )
        self.assertEqual( acd.reason, form_data['reason'] )
#
# fails on codeship:
#
#   >>> django.contrib.auth.models.DoesNotExist: Permission matching query does not exist.
#
# class StaffHasPermissionCashDeposit( AdminPanelCashDeposit ):
#     """
#     test a managers ability to make a CashDepositTransaction
#
#     """
#
#     # >>> Permission.objects.get(name = 'Can add admin cash deposit' ).content_type.model_class().__name__
#     # 'AdminCashDeposit'
#     # >>> Permission.objects.get(name = 'Can add admin cash deposit' ).content_type.model
#     # 'admincashdeposit'
#
#     url         = '/admin/cash/admincashdeposit/add/'
#     user_data   = {
#         'username'      : 'staff',      # subclasses should set the username here
#         'password'      : 'password',       # subclasses should set the password here
#         'is_superuser'  : False,
#         'is_staff'      : True,
#         'permissions'   : [ Permission.objects.get(name = 'Can add admin cash deposit' ) ]
#     }
#     amount      = 2.99


class AdminPanelCashWithdrawal(AbstractTest):
    """
    Test the AdminCashWithdrawalForm for validity

    """

    c       = Client()
    url     = '/thinking_face/cash/admincashwithdrawal/add/'
    amount = 1.00

    def setUp(self):
        super().setUp()
        # nothing much to do here
        pass

    def __user_exists(self, username):
        try:
            u = User.objects.get( username=username )
            return True
        except User.DoesNotExist:
            return False

    def __get_or_create_user_with_perm(self, username='', password='',
                                       is_superuser=False, is_staff=False, permissions=[]):
        #
        # get the user if they exist.
        # if they dont exist, create them with the specified status and permissions
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=password)
            if is_superuser:
                # superuser, by default is also staff
                user.is_superuser   = True
                user.is_staff       = True
            elif is_staff == True and is_superuser == False:
                # staff , but not super user
                user.is_superuser = False
                user.is_staff = True

                # if there are specified permissions, apply them to the staff
                for perm in permissions:
                    user.user_permissions.add( perm )

            else:
                # basic user
                user.is_superuser = False
                user.is_staff   = False

            user.save()
        return user

    def test_admin_add_cash_withdrawal_view(self):
        self.assertEquals( self.__user_exists( 'admin' ), False )

        admin = self.get_admin_user()

        self.assertEquals( self.c.login( username=admin.username, password=self.get_password() ), True )

        # confirm again the person we think is logged in really is:
        logged_in_user_id = None
        for tup in self.c.session.items():
            if tup[0] == '_auth_user_id':
                logged_in_user_id = tup[1]
        self.assertEquals( logged_in_user_id, '%s' % str(admin.pk) )

        #
        ################ deposit
        form_data = {
            'user'      : admin.pk,          # set later on when the user is created
            'amount'    : self.amount,
            'reason'    : 'testing-%s' % self.__class__.__name__
        }
        #form_data['user'] = admin.pk

        try:
            response = self.c.post( AdminPanelCashDeposit.url, form_data )
        except AttributeError:
            pass

        #
        # check if there are ANY new AdminCashDeposits in the database
        acds = AdminCashDeposit.objects.all()
        print('%s - total AdminCashDeposit objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        acd = AdminCashDeposit.objects.get ( user=admin, reason=form_data['reason'] )
        print( acd )
        self.assertEqual( acd.reason, form_data['reason'] )

        #
        ################ withdrawal
        form_data = {
            'user'      : admin.pk,          # set later on when the user is created
            'amount'    : self.amount,
            'reason'    : 'testing-%s' % self.__class__.__name__
        }
        #form_data['user'] = admin.pk

        #
        # in django 1.8...
        # there is a problem with a built in method get_language() somewhere deep in Client
        #  and it throws AttributeError - lets just catch that, because we still should have worked
        try:
            response = self.c.post( self.url, form_data )
        except AttributeError:
            pass

        #
        # check if there are ANY new AdminCashWithdrawals in the database
        acds = AdminCashWithdrawal.objects.all()
        print('%s - total AdminCashWithdrawal objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        acd = AdminCashWithdrawal.objects.get( user=admin, reason=form_data['reason'] )
        print( acd )
        self.assertEqual( acd.reason, form_data['reason'] )

# class StaffHasPermissionCashWithdrawal( AdminPanelCashWithdrawal ):
#     """
#     test a managers ability to make a CashWithdrawalTransaction
#
#     """
#
#     # >>> Permission.objects.get(name = 'Can add admin cash withdrawal' ).content_type.model_class().__name__
#     # 'AdminCashWithdrawal'
#     # >>> Permission.objects.get(name = 'Can add admin cash withdrawal' ).content_type.model
#     # 'admincashwithdrawal'
#
#     url         = '/admin/cash/admincashwithdrawal/add/'
#     user_data   = {
#         'username'      : 'staff',      # subclasses should set the username here
#         'password'      : 'password',       # subclasses should set the password here
#         'is_superuser'  : False,
#         'is_staff'      : True,
#         'permissions'   : [ Permission.objects.get(name = 'Can add admin cash withdrawal' ) ]
#     }
#     amount      = 2.99
