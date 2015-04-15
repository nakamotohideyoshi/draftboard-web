import unittest
import decimal
from django.contrib.auth.models import User
from cash.classes import CashTransaction
from cash.models import CashBalance, CashTransactionDetail
from transaction.exceptions import IncorrectVariableTypeException
import django.test
from cash.forms import AdminCashDepositForm
from cash.admin import AdminCashDepositFormAdmin
from cash.models import AdminCashDeposit, AdminCashWithdrawal
from test.classes import AbstractTest

from django.test.client import Client
from django.test import RequestFactory
from django.contrib import admin
from django.contrib.auth.models import Permission

class CashTransactionTest(AbstractTest):
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
        user = self.get_user(USERNAME)



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

class DepositViewTest(AbstractTest):
    """
    TODOs
        - Amount Field
            -No amount
            -Improper value
            -Max amount
            -Min amount
        - payment_method_nonce
            - missing
            - incorrect
        - Test being logged out
    """
    pass

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
    url     = '/admin/cash/admincashdeposit/add/'
    user_data = {
        'username'      : 'admin',      # subclasses should set the username here
        'password'      : 'password',      # subclasses should set the password here
        'is_superuser'  : True,
        'is_staff'      : True,
        'permissions'   : []            # superusers will have all permissions regardless of this list
    }
    amount = 1.00

    def setUp(self):
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

class StaffHasPermissionCashDeposit( AdminPanelCashDeposit ):
    """
    test a managers ability to make a CashDepositTransaction

    """

    # >>> Permission.objects.get(name = 'Can add admin cash deposit' ).content_type.model_class().__name__
    # 'AdminCashDeposit'
    # >>> Permission.objects.get(name = 'Can add admin cash deposit' ).content_type.model
    # 'admincashdeposit'

    url         = '/admin/cash/admincashdeposit/add/'
    user_data   = {
        'username'      : 'staff',      # subclasses should set the username here
        'password'      : 'password',       # subclasses should set the password here
        'is_superuser'  : False,
        'is_staff'      : True,
        'permissions'   : [ Permission.objects.get(name = 'Can add admin cash deposit' ) ]
    }
    amount      = 2.99


class AdminPanelCashWithdrawal(AbstractTest):
    """
    Test the AdminCashWithdrawalForm for validity

    """

    c       = Client()
    url     = '/admin/cash/admincashwithdrawal/add/'
    amount = 1.00

    def setUp(self):
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

"""
##### class hierarchy ####
class NeedsUser(django.test.TestCase):

    def __init__(self):
        # create a superuser
        pass

class NeedsBalance(NeedsUser):

    def __init__(self, initial_balance=100.00):
        super().__init__()
        self.intiial_balance = initial_balance

    def setUp(self):
        # make a CashTransaction thats a deposit
        pass

class TestWithdraw( NeedsUser, NeedsBalance ):
    rng = range(-100000, 1000000)
    def __init__(self, amount=0.00):
        super().__init__()
        # now somewhere you can have a test method that creates withdraw

    def test_withdraw_xxx(self):
        pass # TODO

class Withdraw1000(TestWithdraw):
    amount = 1000
class Withdraw2000(TestWithdraw):
    amount = 2000
class Withdraw1000(TestWithdraw):
    amount = 3000
"""


"""
class AdminPanelCashDeposit(django.test.TestCase):


    c       = Client()
    url     = '/admin/cash/admincashdeposit/add/'
    user_data = {
        'username'      : 'admin',      # subclasses should set the username here
        'password'      : 'password',      # subclasses should set the password here
        'is_superuser'  : True,
        'is_staff'      : True,
        'permissions'   : []            # superusers will have all permissions regardless of this list
    }
    amount = 1.00

    def setUp(self):
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

    def test_admin_add_cash_deposit_view(self):
        self.assertEquals( self.__user_exists( self.user_data['username'] ), False )

        #admin = self.get_admin_user(username=self.user_data['username'])

        self.assertEquals( admin.username, self.user_data['username'])


        self.assertEquals( self.c.login( username=self.user_data['username'],
                                    password=self.user_data['password'], ), True )

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

        #
        # in django 1.8...
        # there is a problem with a built in method get_language() somewhere deep in Client
        #  and it throws AttributeError - lets just catch that, because we still should have worked
        perms = admin.user_permissions
        print( 'permissions: is_superuser ', admin.is_superuser )
        print( 'permissions: is_staff     ', admin.is_staff )
        #print( 'permissions count: ', str(len(perms)))
        # for p in perms:
        #     print( p )

        #try:
        response = self.c.post( self.url, form_data )
        #except AttributeError:
        #    pass

        #
        # check if there are ANY new AdminCashDeposits in the database
        acds = AdminCashDeposit.objects.all()
        print('%s - total AdminCashDeposit objects in database' % (str(len(acds))) )
        self.assertEqual( len(acds), 1 )   ### we only expect one item here, because no existing data should exist

        acd = AdminCashDeposit.objects.get ( user=admin, reason=form_data['reason'] )
        print( acd )
        self.assertEqual( acd.reason, form_data['reason'] )
"""