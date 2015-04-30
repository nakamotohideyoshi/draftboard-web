#
# promocode/classes.py

from . import models
from django.contrib.auth.models import User

class Promotion( object ):

    def __init__(self, user):
        self.user = user

    def __get_promo(self, code=''):
        """
        return the matching promotion model if it exists.

        raises PromotionDoesNotExistException if it does not match any promos
        raises InvalidPromotionException if the code is not enabled, has expired

        :param code:
        :return:
        """
        pass

    def apply(self, code=''):
        """
        apply this promotion code to the user's account

        :param code:
        :return:
        """
        pass
    