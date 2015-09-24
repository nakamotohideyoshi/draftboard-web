#
# optimal_payments/tests.py

from django.utils import timezone
from datetime import timedelta

from django.test import TestCase
from optimal_payments.classes import CardPurchase

class CardPaymentArguments(TestCase):
    """
    test the Optimal Payments class that processes credit card payments

    ie:

    cp = CardPurchase()    amt      cc_num          cvv   mo.   year   billing-zipcode
    cp.process_purchase( 5.00, '4530910000012345', '111', '11','2016','12345' )
    """

    def setUp(self):
        self.future_date = timezone.now() + timedelta(hours=24*30*12* 13) # 13 months in the future (arbitrary)

        # float or string is valid, as long as there are no decimals past the 100ths
        self.valid_amount       = '5.00'

        # valid Visa test credit card
        self.valid_visa_cc_num  = CardPurchase.TEST_VISA

        # valid test cvv
        self.valid_cvv = '111'
        found = False
        for cvv_code, description in CardPurchase.TEST_CVV_NUMBERS:
            if self.valid_cvv == str(cvv_code):
                found = True
                break
        if not found:
            raise Exception('CardPurchase.TEST_CVV_NUMBERS does not contain the "cvv" code: %s' % self.valid_cvv)

        # any MM/YYYY combo is valid if its greater than the current MM/YYYY !
        self.valid_exp_month    = self.future_date.month
        self.valid_exp_year     = self.future_date.year

        # its made up, but its formatted to be valid (ie: a 5 character string)
        self.valid_zipcode    = '12345'

        # this should work, but mostly we will be test edge cases and making sure
        # InvalidArgumentException is thrown where it should be
        # >>> cp.process_purchase( 5.001, '4530910000012345', '111', '11','2016', self.valid_zipcode )

    def test_amount_fractional_pennies_from_float(self):
        """
        raise InvalidArgumentException if there are decimals past the pennies part of a float
        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( 5.001, self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  self.valid_zipcode ) )

    def test_amount_fractional_pennies_from_str(self):
        """
        raise InvalidArgumentException if there are decimals past the pennies part of a float string
        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( '5.001', self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  self.valid_zipcode ) )

    def test_amount_unparseable_value_str(self):
        """

        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( 'f5.001', self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  self.valid_zipcode ) )

    def test_cc_num_less_than_15_digits(self):
        """
        test a 14 digit cc number
        """
        cc_num_14_digits = '12345678901234'
        cp = CardPurchase()                                         # 14 digits
        self.assertRaises( CardPurchase.InvalidArgumentException,   #   \/
                lambda: cp.process_purchase( self.valid_amount, cc_num_14_digits, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  self.valid_zipcode ) )

    def test_cc_num_more_than_16_digits(self):
        """
        test a 14 digit cc number
        """
        cc_num_17_digits = '12345678901234567'
        cp = CardPurchase()                                         # 17 digits
        self.assertRaises( CardPurchase.InvalidArgumentException,   #   \/
                lambda: cp.process_purchase( self.valid_amount, cc_num_17_digits, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  self.valid_zipcode ) )

    def test_expiration_month_year_same_as_actual_date(self):
        """

        """
        now         = timezone.now().date()
        this_month  = now.month
        this_year   = now.year

        cp = CardPurchase()
        self.assertRaises( CardPurchase.ExpiredCreditCardException,
                lambda: cp.process_purchase( self.valid_amount, self.valid_visa_cc_num, self.valid_cvv,
                             this_month, this_year,  self.valid_zipcode ) )

    def test_expiration_month_year_older_than_actual_date(self):
        """

        """
        dt_now      = timezone.now() - timedelta(days=31)
        now         = dt_now.date()
        this_month  = now.month
        this_year   = now.year

        cp = CardPurchase()
        self.assertRaises( CardPurchase.ExpiredCreditCardException,
                lambda: cp.process_purchase( self.valid_amount, self.valid_visa_cc_num, self.valid_cvv,
                             this_month, this_year,  self.valid_zipcode ) )

    def test_zipcode_not_5_characters(self):
        """
        zipcodes should have 5 characters
        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( self.valid_amount, self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  '0000' ) )

    def test_zipcode_contains_non_numerics(self):
        """
        zipcodes should have 5 characters
        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( self.valid_amount, self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  '0f000' ) )

    def test_zipcode_passed_as_integer(self):
        """
        it needs to be a string in case of a leading 0
        """
        cp = CardPurchase()
        self.assertRaises( CardPurchase.InvalidArgumentException,
                lambda: cp.process_purchase( self.valid_amount, self.valid_visa_cc_num, self.valid_cvv,
                             self.valid_exp_month, self.valid_exp_year,  1234 ) )

