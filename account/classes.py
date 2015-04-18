#
# this class is responsible for the objects which manipulate underlying data.
# there are probably many helper methods contained in the classes within this code.

from django.contrib.auth.models import User
from mysite.classes import  AbstractSiteUserClass
from .models import Information
from .exceptions import  AccountInformationException
class UserUtil(object):

    def create_user_master(self, username, email, password):
        user = User.objects.create_user( username=username,
                                         email=email,
                                         password=password )
        return user



class AccountInformation( AbstractSiteUserClass ):
    """
    Class manages the user's account information
    """
    information= None
    def __init__(self, user):
        super().__init__(user)
        self.update_information()

    def update_information(self):
        try:
            self.information = Information.objects.get(user=self.user)
        except Information.DoesNotExist:
            #
            # If the information for the user does not exist, create the object
            self.information = Information()
            self.information.user = self.user
            self.information.save()

    def validate_mailing_address(self):
        """
        Checks to make sure fullname, address1, city, state, and zipcode are filled out
        for the given user. If not it will throw an exception describing the fields missing.


        """
        required_fields = ['fullname', 'address1', 'city', 'state', 'zipcode']

        #
        # Make sure all of the fields are filled out and if there
        # are any missing to add their names to the missing_fields array
        missing_fields = []
        for field in required_fields:
            value = getattr(self.information, field)
            if(value == ''):
                missing_fields.append(field)

        #
        # If we have any missing fields raise the exception containing the fields.
        if(len(missing_fields) > 0):
            raise AccountInformationException(self.user.username, ', '.join(missing_fields) )

    def set_fields(self, fullname='', address1= '', city = '', state= '', zipcode = '', dob = None):
        self.information.fullname    = fullname
        self.information.address1    = address1
        self.information.city        = city
        self.information.state       = state
        self.information.zipcode     = zipcode
        self.information.dob         = dob
        self.information.save()
