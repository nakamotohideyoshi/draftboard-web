from django.test import TestCase

from transaction.models import Transaction, TransactionType
from transaction.constants import TransactionTypeConstants
from test.classes import AbstractTest
import promocode.models
from promocode.classes import PromoManager
from promocode.bonuscash.classes import BonusCashTransaction
from mysite.exceptions import InvalidPromoCodeException, PromoCodeAlreadyUsedException, \
                                PromoCodeExpiredException, CanNotRemovePromoCodeException

from django.utils import timezone

class PromoManagerExceptionsTest( AbstractTest ):

    def setUp(self):
        super().setUp()
        self.transaction_type_promocode_add = \
            TransactionType.objects.get(pk=TransactionTypeConstants.PromoCodeAdd.value)
        self.transaction_type_promocode_remove = \
            TransactionType.objects.get(pk=TransactionTypeConstants.PromoCodeRemove.value)

        self.user   = self.get_admin_user()     # get a superuser
        self.code   = 'PROMOTEST'

    def __get_or_create_promotion(self, code='', enabled=True, first_time_only=True,
                                  expires=None, max_bonuscash=600.0, fpp_per_bonus_dollar=20.0 ):
        if not code:
            code = self.code
        try:
            promotion = promocode.models.Promotion.objects.get( code=code )
        except promocode.models.Promotion.DoesNotExist:
            promotion = promocode.models.Promotion()
            promotion.enabled               = enabled
            promotion.code                  = code
            promotion.first_deposit_only    = first_time_only
            promotion.expires               = expires
            promotion.max_bonuscash         = max_bonuscash
            promotion.fpp_per_bonus_dollar  = fpp_per_bonus_dollar
            promotion.save()
        return promotion

    def test_add_invalid_code(self):
        pm = PromoManager(self.user)
        self.assertRaises( InvalidPromoCodeException, lambda: pm.add( 'SHOULDNTEXIST') )

    def test_add_expired_code(self):
        now = timezone.now()
        promotion = self.__get_or_create_promotion(code=self.code, expires=now)
        pm = PromoManager(self.user)
        self.assertRaises( PromoCodeExpiredException, lambda: pm.add(self.code) )

    def test_add_disabled_code(self):
        promotion = self.__get_or_create_promotion(code=self.code, enabled=False)
        pm = PromoManager(self.user)
        self.assertRaises( InvalidPromoCodeException, lambda: pm.add(self.code) )

    def test_sucessful_add_code(self):
        promotion = self.__get_or_create_promotion(code=self.code)
        pm = PromoManager(self.user)
        pm.add(self.code)

    def test_add_already_used_code(self):
        promotion = self.__get_or_create_promotion(code=self.code)
        pm = PromoManager(self.user)
        pm.add(self.code)

        pm2 = PromoManager(self.user)
        self.assertRaises( PromoCodeAlreadyUsedException, lambda: pm2.add(self.code) )

    def test_double_add_second_add_should_except(self):
        promotion = self.__get_or_create_promotion(code=self.code)
        pm = PromoManager(self.user)
        pm.add(self.code)
        self.assertRaises( PromoCodeAlreadyUsedException, lambda: pm.add(self.code) )

    def test_remove_non_existing_promocode(self):
        pm = PromoManager(self.user)
        self.assertRaises( CanNotRemovePromoCodeException, lambda: pm.remove('SHOULDNTEXIST') )

    def test_add_and_remove_promocode_ensure_transactions_exist(self):
        promotion = self.__get_or_create_promotion(code=self.code)
        pm = PromoManager(self.user)
        new_promocode = pm.add(self.code)
        # ensure "add" transaction exists, and is the right type
        t = Transaction.objects.get(pk=new_promocode.transaction.pk)
        self.assertIsNotNone( t )
        self.assertEquals( t.category, self.transaction_type_promocode_add )

        pm2 = PromoManager(self.user)
        remove_transaction = pm2.remove(self.code)
        # ensure "remove" transaction exists
        remove_transaction = Transaction.objects.get(pk=remove_transaction.pk)
        self.assertIsNotNone(remove_transaction)
        self.assertEquals( remove_transaction.category, self.transaction_type_promocode_remove)
