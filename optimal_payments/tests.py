#
# optimal_payments/tests.py

from django.utils import timezone
from datetime import timedelta

from django.test import TestCase
from optimal_payments.classes import CardPurchase

#
# Important:
# force the test/sandbox environemtn for test.py !
CardPurchase._environment = 'TEST'

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

#
# test all the known response codes for Optimal
#
# source: https://developer.optimalpayments.com/en/documentation/card-payments-api/simulating-response-codes/
class CardPaymentResponses(TestCase):
    """
    test OptimalPayments credit card payment processing response information

    "Minor Units" are what Optimal refers to a lot.
    An amount of $0.01 is equal to 1 "Minor Unit"
    """

    #
    # WARNING:
    #
    #  changing the values in this list affects nothing!
    #  its mainly for readability, but it should be accurate.
    #
    RESPONSE_INFO = [
        # ( Amount in $USD,     HTTP status code,   Error code,     Response msg )
        ( '0.01',               200,                None,           'Approved' ),
        ( '0.04',               402,                3015,           'The bank has requested that you process the transaction manually by calling the ard holders cc company' ),
        ( '0.05',               402,                3009,           'Your request has been declined by the issuing bank'),
        ( '0.06',               500,                1007,           'Clearing house timeout (although the simulator returns immediately; if delay is required see amount 96)'),
        ( '0.11',               402,                3022,           'The card has been declined due to insufficient funds'),
        ( '0.12',               402,                3023,           'declined by issuing bank - proprietary usage reasons'),
        ( '0.13',               402,                3024,           'declined by issuing bank - does not permit the transaction for this card.'),
        ( '0.20',               500,                1007,           'internal error occurred'),
        ( '0.23',               402,                4002,           'declined by our risk management team'),
        ( '0.24',               402,                3007,           'your request failed the AVS check'),
        ( '0.25',               402,                4001,           'the card # or email address associated is in our negative database'),
        #
        # 90 - 96 are 5 thru 35 second delay, in 5 second incrememnts
        ( '0.91',               500,                1007,           'declined - test delay'), # 10 second delay
    ]

    def __process_amount(self, amount):
        """
        call process_purchase with valid static param, but with the amount specified
        """
        cp = CardPurchase()
        dt = timezone.now() + timedelta(days=500)
        d = dt.date()
        month   = str(d.month).zfill(2)
        year    = str(d.year)
        cp.process_purchase( amount, '4530910000012345', '111', month, year,'03055' )

    def test_error_code_3015(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.04'))


    def test_error_code_3009(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.05'))

    def test_error_code_1007(self):
        """

        """
        self.assertRaises( CardPurchase.ProcessingException,
                           lambda: self.__process_amount('0.06'))

    def test_error_code_3022(self):
        """
        sometimes this throws ProcessingException, strangely !
        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.11'))

    def test_error_code_3023(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.12'))

    def test_error_code_3024(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.13'))

    def test_error_code_4002(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.23'))

    def test_error_code_3007(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.24'))

    def test_error_code_4001(self):
        """

        """
        self.assertRaises( CardPurchase.PaymentDeclinedException,
                           lambda: self.__process_amount('0.25'))