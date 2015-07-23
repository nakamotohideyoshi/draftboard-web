from django.contrib.auth.models import User
from mysite.exceptions import IncorrectVariableTypeException

class AbstractSiteUserClass( object ):

    def __init__(self, user):
        """
        Initializes the variables
        :param user:
        :return:
        """
        #
        # Validate that user and category are proper types
        if(not isinstance(user, User)):
            raise IncorrectVariableTypeException(type(self).__name__,
                                          "user")

        self.user = user

    def validate_variable(self, expected_class, variable=None):
        if variable is not None:
            #
            # validate the contest is an instance of contest.models.Contest
            if not isinstance(variable, expected_class):
                raise IncorrectVariableTypeException(
                    type(self).__name__,
                    'contest')