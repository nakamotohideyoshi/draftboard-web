from django.contrib.auth.models import User
from mysite.exceptions import IncorrectVariableTypeException
from django.conf import settings


class AbstractManagerClass( object ):

    def __init__(self):
        pass

    def validate_variable(self, expected_class, variable=None):
        if variable is not None:
            #
            # validate the contest is an instance of contest.models.Contest
            if not isinstance(variable, expected_class):
                raise IncorrectVariableTypeException(
                    type(self).__name__,
                    'contest')

    def validate_variable_array(self, expected_class, variable_array=[]):
        self.validate_variable(list, variable_array)
        for variable in variable_array:
            #
            # validate the contest is an instance of contest.models.Contest
            if not isinstance(variable, expected_class):
                raise IncorrectVariableTypeException(
                    type(self).__name__,
                    'contest')

    def get_escrow_user(self):
        return User.objects.get(username=settings.USERNAME_ESCROW)

    def get_draftboard_user(self):
        return User.objects.get(username=settings.USERNAME_DRAFTBOARD)


class AbstractSiteUserClass( AbstractManagerClass ):

    def __init__(self, user):
        """
        Initializes the variables
        :param user:
        :return:
        """
        #
        # Validate that user and category are proper types
        self.validate_variable(User, user)


        self.user = user





