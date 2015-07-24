import django.test
from django.contrib.auth.models import User
import threading
from django.db import connections

class MasterAbstractTest():

    PASSWORD = 'password'
    def get_user(self, username='username', is_superuser=False,
                 is_staff=False, permissions=[]):
        #
        # get the user if they exist.
        # if they don't exist, create them with the specified status and permissions
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username, password=self.PASSWORD)
            user.email = 'admin@test.com'
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

    def get_admin_user(self, username='admin'):
        user = self.get_user(username=username, is_superuser=True,
                        is_staff=True)
        return user

    def get_staff_user(self, username='staff', permissions=[]):
        user = self.get_user(username=username, is_superuser=False,
                        is_staff=True, permissions=permissions)
        return user

    def get_basic_user(self, username='basic'):
        user = self.get_user(username=username, is_superuser=False,
                        is_staff=False)
        return user

    def get_alternate_user(self, existing_user):
        """
        return a user who is different from the existing user argument,
        by at least its primary key (pk) and username.

        is_superuser & is_staff should also match.

        permissions will not match however

        :param existing_user:
        :return:
        """
        return self.get_user(username=existing_user.username + 'alt',
                             is_superuser=existing_user.is_superuser,
                             is_staff=existing_user.is_staff )

    def get_password(self):
        return self.PASSWORD



class AbstractTest(django.test.TestCase, MasterAbstractTest):

    def setUp(self):
        pass



class AbstractTestTransaction(django.test.TransactionTestCase, MasterAbstractTest):

    def setUp(self):
        pass

    def concurrent_test(self, times, test_func, *args, **kwargs ):
        exceptions = []
        def call_test_func():
            try:
                test_func(*args, **kwargs)
            except Exception as e:
                exceptions.append(e)
                return
            for conn in connections.all():
                conn.close()
        threads = []
        for i in range(times):
            threads.append(threading.Thread(target=call_test_func))
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        return exceptions