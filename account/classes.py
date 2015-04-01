#
# this class is responsible for the objects which manipulate underlying data.
# there are probably many helper methods contained in the classes within this code.

from django.contrib.auth.models import User

class UserUtil(object):

    def create_user_master(self, username, email, password):
        user = User.objects.create_user( username=username,
                                         email=email,
                                         password=password )
        return user