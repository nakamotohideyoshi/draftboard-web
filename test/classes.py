import django.test
from django.contrib.auth.models import User

class AbstractTest(django.test.TestCase):

    PASSWORD = 'password'

    def setUp(self):
        pass

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

    def get_password(self):
        return self.PASSWORD