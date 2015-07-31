#
# promocode/classes.py

import transaction.models
import transaction.constants
import mysite.classes
from promocode.models import Promotion, PromoCode
from django.db import transaction as django_db_transaction   # for 'atomic'
from mysite.exceptions import InvalidPromoCodeException, PromoCodeAlreadyUsedException, \
                                PromoCodeExpiredException, CanNotRemovePromoCodeException

from django.utils import timezone # for timezone.now() which gets current datetime

class PromoManager( mysite.classes.AbstractSiteUserClass ):
    """
    Primarily takes care of adding PromoCodes to a User.

    Note, this class can NOT create BonusCashTransactions,
    because PromoCodes are applied to an account before
    a deposit of funds is made!

    This means that whatever mechanimsm is performing
    the real cash funds deposit needs to check what existing
    promotions may be associated with this user.

    >>> TODO - should this class have a function which adds the bonuscash?

    """

    def __init__(self, user):
        super().__init__(user) # gives us self.user

    def __get_promotion(self, code=''):
        try:
            p = Promotion.objects.get(code=code)
        except Promotion.DoesNotExist:
            raise InvalidPromoCodeException(type(self).__name__, code)
        return p

    def __already_used(self, code=''):
        """
        return True if this code has already been used by the user

        :param code:
        :return:
        """
        try:
            exiting_promocode = PromoCode.objects.get( user=self.user, promotion__code=code )
            return exiting_promocode
        except PromoCode.DoesNotExist:
            pass # because we are glad it doesnt exist
        return None

    def __can_use_code(self, code=''):
        promotion = self.__get_promotion(code)

        if not promotion.enabled:
            raise InvalidPromoCodeException(type(self).__name__, code)

        if promotion.expires and promotion.expires <= timezone.now():
            raise PromoCodeExpiredException(type(self).__name__, code)

        # try:
        #     x = PromoCode.objects.get( user=self.user, promotion__code=code )
        #     raise PromoCodeAlreadyUsedException(type(self).__name__, code)
        # except PromoCode.DoesNotExist:
        #     pass # because we are glad it doesnt exist
        if self.__already_used(code=code):
            raise PromoCodeAlreadyUsedException(type(self).__name__, code)

        return promotion

    def __transaction_type_add(self):
        return transaction.models.TransactionType.objects.get(
                    pk=transaction.constants.TransactionTypeConstants.PromoCodeAdd.value )

    def __transaction_type_remove(self):
        return transaction.models.TransactionType.objects.get(
                    pk=transaction.constants.TransactionTypeConstants.PromoCodeRemove.value )

    @django_db_transaction.atomic
    def __add_promocode(self, promotion):
        #
        # create the transaction
        t = transaction.models.Transaction()
        t.user      = self.user
        t.category  = self.__transaction_type_add()
        t.save()

        #
        # create the promocode and return it
        promocode = PromoCode()
        promocode.user          = self.user
        promocode.promotion     = promotion
        promocode.transaction   = t
        promocode.save()

        return promocode

    def used_codes(self):
        """
        get the list of PromoCode models the user has already used
        """
        return PromoCode.objects.filter( user=self.user )

    def add(self, code=''):
        """
        add this promotion for the user

        :param code:
        :return:
        :raises :class: `mysite.exceptions.InvalidPromoCodeException`:
        :raises :class: `mysite.exceptions.PromoCodeAlreadyUsedException`:
        :raises :class: `mysite.exceptions.PromoCodeExpiredException`:
        """

        #
        # throws exceptions if its invalid, expired, or already used
        promotion = self.__can_use_code(code)
        return self.__add_promocode(promotion) # returns the new PromoCode

    def remove(self, code=''):
        """
        all this method does is add a PromoCode removed transaction. thats it. no other side effects!

        does not add/modify/remove any cash OR bonus cash or anything which
        may have resulted from the PromoCode being in place for any amount of time!

        :param code:
        :return:
        """
        t = None
        existing_promocode = self.__already_used(code=code)
        if existing_promocode:
            #
            # add the remove transaction
            t = transaction.models.Transaction()
            t.user      = self.user
            t.category  = self.__transaction_type_remove()
            t.save()
        else:
            raise CanNotRemovePromoCodeException(type(self).__name__, code)

        return t      # return the new transaction, else None
