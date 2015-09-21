#
# optimal_payments/classes.py

from django.conf import settings

from PythonNetBanxSDK.OptimalApiClient import OptimalApiClient
from PythonNetBanxSDK.CardPayments.Authorization import Authorization
from PythonNetBanxSDK.CardPayments.Pagination import Pagination
from PythonNetBanxSDK.CardPayments.AuthorizationReversal import AuthorizationReversal
from PythonNetBanxSDK.CardPayments.Authentication import Authentication
from PythonNetBanxSDK.CardPayments.Verification import Verification
from PythonNetBanxSDK.CustomerVault.Profile import Profile
from PythonNetBanxSDK.CardPayments.Card import Card
from PythonNetBanxSDK.CardPayments.CardExpiry import CardExpiry
from PythonNetBanxSDK.CardPayments.BillingDetails import BillingDetails
from PythonNetBanxSDK.CardPayments.ShippingDetails import ShippingDetails

import random
import string

#
# source: https://developer.optimalpayments.com/en/sdk/server-side/python/card-payments-api/

class RandomTokenGenerator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def generateToken(self):
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
        return (token)

class CardPurchase(object):
    """
    This class can process credit card purchases, using Optimal Payments API

    test information source:

        https://developer.optimalpayments.com/en/documentation/web-services-api/testing/
    """

    BILLING_ZIPCODE_LENGTH = 5      # the zipcode should be 5 characters in length

    TEST_VISA   = 4530910000012345
    TEST_VISA_2 = 4510150000000321
    TEST_CVV_NUMBERS = [
        (111, 'match'),
        (222, 'not processed'),
        (333, 'value should be on card but was not provided'),
        (444, 'issue not certified'),
        (555, 'unknown response'),
        (666, 'no match')
    ]

    RESPONSE_STATUS = 'status'
    MONITOR_READY   = 'READY'

    # Static data
    _environment    = settings.OPTIMAL_ENVIRONMENT      # 'TEST' or 'LIVE'
    _api_key        = settings.OPTIMAL_API_KEY          #'devcentre4628'
    _api_password   = settings.OPTIMAL_API_PASSWORD     # 'B-qa2-0-548ef25d-302b0213119f70d83213f828bc442dfd0af3280a7b48b1021400972746f9abe438554699c8fa3617063ca4c69a'
    _account_number = settings.OPTIMAL_ACCOUNT_NUMBER   # '89983472'

    # the api service is not currently accessible
    class OptimalServiceMonitorDownException(Exception): pass

    # the monitor is not responding with "READY" status
    class OptimalServiceMonitorNotReadyException(Exception): pass

    # raised when a function argument is invalid for whatever reason
    class InvalidArgumentException(Exception): pass

    def __init__(self):
        '''
        Constructor
        '''
        print('OptimalPayments: %s' % settings.OPTIMAL_ENVIRONMENT)

        self.optimal_obj = None

    def approx_equal(self, a, b, tol):
        return abs(a-b) <= max(abs(a), abs(b)) * tol

    def __validate_amount(self, amt):
        """

        :param amt:
        :return:
        """
        original_amt = amt
        if amt is None:
            raise self.InvalidArgumentException('the amount specified cant be None')

        if isinstance(amt, str):
            # convert to float, and multiply by 100
            try:
                amt = float(amt)
            except ValueError:
                raise self.InvalidArgumentException('amt [%s] could not be convert to a number' % str(amt))

        if isinstance(amt, float):
            tmp     = amt * 100.0   # will retain decimal places 0.001 and out
            amt     = int( tmp )
            #print( tmp, amt )
            if not self.approx_equal(tmp, amt, 0.00001):
                raise self.InvalidArgumentException('amt [%s] would truncate fractional pennies. please specify values to the 0.01 decimal place' % str(original_amt))

        if isinstance(amt, int):
            # ensure the amount is not None, and that its an Integer value
            pass

        else:
            raise self.InvalidArgumentException('the amount must be either a str, int or a float')

        return amt

    def __validate_credit_card_number(self, cc_num):
        """

        :param cc_num:
        :return:
        """
        if isinstance(cc_num, int):
            cc_num = str(cc_num)

        if cc_num is None or not isinstance(cc_num, str):
            raise self.InvalidArgumentException('invalid type for cc_num: ', cc_num.__class__.__name__)

        # its a string at this point, remove leading/trailing whitespace
        cc_num = cc_num.strip()
        num_digits = len(cc_num)
        if num_digits < 15 or num_digits > 16:
            # reject cards without 15 or 16 digits
            msg = 'credit card number [%s] should have 15 or 16 digits. you gave %s' % (str(cc_num), str(num_digits))
            raise self.InvalidArgumentException(msg)

        return cc_num

    def __validate_zipcode(self, billing_zipcode):
        """

        :param billing_zipcode:
        :return:
        """

        # make sure zipcode does not come in as a number,
        # because there could be a leading 0 we must capture
        if billing_zipcode is None or not isinstance(billing_zipcode, str):
            # the zipcode is not a string
            raise self.InvalidArgumentException('the zipcode must be a string')

        billing_zipcode = billing_zipcode.strip()
        if len(billing_zipcode) != self.BILLING_ZIPCODE_LENGTH:
            raise self.InvalidArgumentException('the zipcode must contain 5 characters: ' % billing_zipcode)

        try:
            billing_zipcode = int(billing_zipcode)
        except TypeError:
            raise self.InvalidArgumentException('the zipcode must only contain numerical characters: ' % billing_zipcode)

        return billing_zipcode

    def process_purchase_test(self, amt, cc_num, cvv,
                                      exp_month, exp_year,
                                      billing_zipcode,
                                      settleWithAuth=True):
        """
        process the purchase amount with the given credit card information.

        the 'amt' specified should be the intuitive amount, ie: 55.34,
        although internally this method will multiply by 100 and truncate remaining decimal places!

        :param amt:
        :param settleWithAuth:
        :param cc_num:
        :param cvv:
        :param exp_month:
        :param exp_year:
        :param billing_zipcode:
        :return:
        """
        # validate the arguments passed in here for type, and size validity,
        # but let the API do the rest of the work.
        amt_hundreds    = self.__validate_amount( amt )
        cc_num          = self.__validate_credit_card_number( cc_num )
        billing_zipcode = self.__validate_zipcode( billing_zipcode )

        return None

        #
        # ensure the payemnts api is ready by checking status of the card payments monitor
        self.card_payments_monitor()

        #
        # build the card purchase
        auth_obj = Authorization(None)
        card_obj = Card(None)
        cardExpiry_obj = CardExpiry(None)
        billing_obj = BillingDetails(None)
        auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
        auth_obj.amount(str(amt_hundreds))
        auth_obj.settleWithAuth("true" if settleWithAuth else "false")
        card_obj.cardNum(str(cc_num))
        card_obj.cvv(str(cvv))
        auth_obj.card(card_obj)
        cardExpiry_obj.month(str(exp_month))
        cardExpiry_obj.year(str(exp_year))
        card_obj.cardExpiry(cardExpiry_obj)
        billing_obj.zip(billing_zipcode)
        auth_obj.billingDetails(billing_obj)
        response_object = self.optimal_obj.card_payments_service_handler().create_authorization(auth_obj)
        return response_object

    def card_payments_monitor(self):
        '''
        Card Payments Monitor
        '''
        self.optimal_obj = OptimalApiClient(self._api_key,
                                             self._api_password,
                                             self._environment,    # 'TEST' or 'LIVE'
                                             self._account_number)
        #self._optimal_obj._update_env('www.google.co.in',10,30,30)
        self.response_object = self.optimal_obj.card_payments_service_handler().monitor()
        r = self.response_object.__dict__
        #print("response: ")
        #print(str(r))

        # validate if its up or down
        try:
            status = r.get( self.RESPONSE_STATUS )
        except:
            raise self.OptimalServiceMonitorDownException('Optimal Payment service currently not responding!')
        if status != self.MONITOR_READY:
            raise self.OptimalServiceMonitorNotReadyException('Optimal Payment monitor is not ready -- cannot process transaction')


    # def request_conflict_example_for_auth(self):
    #     '''
    #     Request Conflict Exception
    #     '''
    #     auth_obj = Authorization(None)
    #     card_obj = Card(None)
    #     cardExpiry_obj = CardExpiry(None)
    #     billing_obj = BillingDetails(None)
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("1")
    #     auth_obj.settleWithAuth("false")
    #     card_obj.cardNum("4917480000000008")
    #     card_obj.cvv("123")
    #     auth_obj.card(card_obj)
    #     cardExpiry_obj.month("12")
    #     cardExpiry_obj.year("2017")
    #     card_obj.cardExpiry(cardExpiry_obj)
    #     billing_obj.zip("M5H 2N2")
    #     auth_obj.billingDetails(billing_obj)
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler().create_authorization(auth_obj)
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #     response_object = self._optimal_obj.card_payments_service_handler().create_authorization(auth_obj)
    #     print ("Complete Response : ")
    #     print (response_object.error.code)
    #     print (response_object.error.message)
    #
    #
    # def create_authorization_with_payment_token(self):
    #     '''
    #     Create Authorization with payment token
    #     '''
    #     auth_obj = Authorization(None)
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("1200")
    #
    #     card_obj = Card(None)
    #     card_obj.paymentToken("C7dEdq9Mcz4nwyy")
    #
    #     auth_obj.card(card_obj)
    #
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #     print ("Card ID: ", response_object.card.__dict__)
    #
    #
    # def create_complex_authorization(self):
    #     '''
    #     Create Complex Authorization
    #     '''
    #     auth_obj = Authorization(None)
    #     authentication_obj = Authentication(None)
    #     card_obj = Card(None)
    #     cardExpiry_obj = CardExpiry(None)
    #     billing_obj = BillingDetails(None)
    #     shipping_obj = ShippingDetails(None)
    #
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("5")
    #     auth_obj.settleWithAuth("false")
    #     auth_obj.customerIp("204.91.0.12")
    #
    #     card_obj.cardNum("5036150000001115")
    #     card_obj.cvv("123")
    #     auth_obj.card(card_obj)
    #
    #     cardExpiry_obj.month("4")
    #     cardExpiry_obj.year("2017")
    #     card_obj.cardExpiry(cardExpiry_obj)
    #
    #     authentication_obj.eci("5")
    #     authentication_obj.cavv("AAABCIEjYgAAAAAAlCNiENiWiV+=")
    #     authentication_obj.xid("OU9rcTRCY1VJTFlDWTFESXFtTHU=")
    #     authentication_obj.threeDEnrollment("Y")
    #     authentication_obj.threeDResult("Y")
    #     authentication_obj.signatureStatus("Y")
    #     auth_obj.authentication(authentication_obj)
    #
    #     billing_obj.street("100 Queen Street West")
    #     billing_obj.city("Toronto")
    #     billing_obj.state("ON")
    #     billing_obj.country("CA")
    #     billing_obj.zip("M5H 2N2")
    #     auth_obj.billingDetails(billing_obj)
    #
    #     shipping_obj.carrier("FEX")
    #     shipping_obj.shipMethod("C")
    #     shipping_obj.street("100 Queen Street West")
    #     shipping_obj.city("Toronto")
    #     shipping_obj.state("ON")
    #     shipping_obj.country("CA")
    #     shipping_obj.zip("M5H 2N2")
    #     auth_obj.shippingDetails(shipping_obj)
    #
    #     #self.optimal_obj.card_payments_service_handler().lookup_authorization_with_id(auth_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    #
    # def create_authorization_with_card(self):
    #     '''
    #     Create Authorization with payment token
    #     '''
    #
    #     auth_obj = Authorization(None)
    #     card_obj = Card(None)
    #     cardExpiry_obj = CardExpiry(None)
    #     billing_obj = BillingDetails(None)
    #
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("1400")
    #     auth_obj.settleWithAuth("false")
    #
    #     card_obj.cardNum("4530910000012345")
    #     card_obj.cvv("123")
    #     auth_obj.card(card_obj)
    #
    #     cardExpiry_obj.month("2")
    #     cardExpiry_obj.year("2017")
    #     card_obj.cardExpiry(cardExpiry_obj)
    #
    #     billing_obj.zip("M5H 2N2")
    #     auth_obj.billingDetails(billing_obj)
    #
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #     print ("Card ID: ", response_object.card.__dict__)
    #
    # def payment_process_with_card_settle_with_auth_true(self):
    #     '''
    #     Process a card purchase (settleWithAuth=true)
    #     '''
    #
    #     auth_obj = Authorization(None)
    #     card_obj = Card(None)
    #     cardExpiry_obj = CardExpiry(None)
    #     billing_obj = BillingDetails(None)
    #
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("4")
    #     auth_obj.settleWithAuth("true")
    #
    #     card_obj.cardNum("4530910000012345")
    #     card_obj.cvv("123")
    #     auth_obj.card(card_obj)
    #
    #     cardExpiry_obj.month("2")
    #     cardExpiry_obj.year("2017")
    #     card_obj.cardExpiry(cardExpiry_obj)
    #
    #     billing_obj.zip("M5H 2N2")
    #     auth_obj.billingDetails(billing_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #     print ("Card ID: ", response_object.card.__dict__)
    #     print("error code: ", response_object.error.code)
    #     print("error message: ", response_object.error.message)
    #
    #
    # def partial_authorization_reversal(self):
    #     '''
    #     Partial authorization reversal
    #     '''
    #     auth_obj = Authorization(None)
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount(555)
    #     auth_obj.settleWithAuth("false")
    #
    #     card_obj = Card(None)
    #     card_obj.cardNum("4530910000012345")
    #     card_obj.cvv("123")
    #     auth_obj.card(card_obj)
    #
    #     cardExpiry_obj = CardExpiry(None)
    #     cardExpiry_obj.month("1")
    #     cardExpiry_obj.year("2017")
    #     card_obj.cardExpiry(cardExpiry_obj)
    #
    #     billing_obj = BillingDetails(None)
    #     billing_obj.zip("M5H 2 N2")
    #     auth_obj.billingDetails(billing_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Authorization Response : ", response_object.__dict__)
    #     auth_id = response_object.id
    #     print ("Authorization Id : ", auth_id)
    #     # dea6fd3a-3e47-4b44-a303-c5c38f7104f6
    #     auth_rev =  AuthorizationReversal(None)
    #     auth_rev.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_rev.amount(222)
    #
    #     auth_obj2 = Authorization(None)
    #     auth_obj2.id(auth_id)
    #     auth_rev.authorization(auth_obj2)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).reverse_authorization_using_merchant_no(auth_rev)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    #
    #
    # def lookup_authorization_with_id(self):
    #     '''
    #     Lookup Authorization with Id
    #     '''
    #     auth_obj = Authorization(None)
    #     auth_obj.id("5406f84a-c728-499e-b310-c55f4e52af9f")
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).lookup_authorization_with_id(auth_obj)
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    #
    #
    #
    # def lookup_authorization_with_merchant_ref_num(self):
    #     '''
    #     Lookup Authorization with Id
    #     '''
    #     pagination_obj = Pagination(None)
    #     #pagination_obj.limit = "4"
    #     #pagination_obj.offset = "0"
    #     #pagination_obj.startDate = "2015-02-10T06:08:56Z"
    #     #pagination_obj.endDate = "2015-02-20T06:08:56Z"
    #     #f0yxu8w57de4lris
    #     #zyp2pt3yi8p8ag9c
    #     auth_obj = Authorization(None)
    #     auth_obj.merchantRefNum("f0yxu8w57de4lris")
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).lookup_authorization_with_merchant_no(auth_obj, pagination_obj)
    #     print ("Complete Response : ")
    #     print (response_object)
    #     #print (response_object.links[0].rel)
    #     #print (response_object.links[0].href)
    #     #print (response_object[0].links[0].href)
    #     print (response_object[0].__dict__)
    #     #print (response_object.error.fieldErrors[0].__dict__)
    #     #print (response_object.error.fieldErrors[1].__dict__)
    #
    #
    #
    # def complete_authorization(self):
    #     '''
    #     Complete
    #     '''
    #     auth_obj = Authorization(None)
    #     auth_obj.id("55b77870-266c-4796-bce1-008334aad424")
    #     auth_obj.status("COMPLETED")
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).complete_authorization_request(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    #
    #
    # def settle_authorization(self):
    #     '''
    #     Settle an Authorization
    #     '''
    #     auth_obj = Authorization(None)
    #     auth_obj.id("55b77870-266c-4796-bce1-008334aad424")
    #     auth_obj.merchantRefNum("5m8652wc1pirizft")
    #     auth_obj.amount("500")
    #     #auth_obj.dupCheck(True)
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).settle_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    # def verify_card_billing_details(self):
    #     '''
    #     Sample of verifying a card and billing details
    #     '''
    #     verify_obj = Verification(None)
    #     card_obj = Card(None)
    #     card_exp_obj = CardExpiry(None)
    #     billing_obj = BillingDetails(None)
    #     profile_obj = Profile(None)
    #
    #     verify_obj.merchantRefNum("4lnvozq01d1pbkr0")
    #     #verify_obj.customerIp("204.91.0.12")
    #     #verify_obj.description("This is  a test transaction")
    #
    #     #profile_obj.firstName("John")
    #     #profile_obj.lastName("Smith")
    #     #profile_obj.email("john.smith@somedomain.com")
    #     #verify_obj.profile(profile_obj)
    #
    #     card_obj.cardNum("4530910000012345")
    #     card_obj.cvv("123")
    #     verify_obj.card(card_obj)
    #
    #     card_exp_obj.month("02")
    #     card_exp_obj.year("2017")
    #     card_obj.cardExpiry(card_exp_obj)
    #
    #     #billing_obj.street("100 Queen Street West")
    #     #billing_obj.city("Toronto")
    #     #billing_obj.state("ON")
    #     #billing_obj.country("CA")
    #     billing_obj.zip("M5H 2N2")
    #     verify_obj.billingDetails(billing_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).verify_card(verify_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    # def verify_card_using_payment_token(self):
    #     '''
    #     Sample of verifying a card using payment token
    #     '''
    #     verify_obj = Verification(None)
    #     card_obj = Card(None)
    #     #card_exp_obj = CardExpiry(None)
    #     #billing_obj = BillingDetails(None)
    #     #profile_obj = Profile(None)
    #     #shipping_obj = ShippingDetails(None)
    #
    #     verify_obj.merchantRefNum("rp12jb19igryjqff")
    #     card_obj.paymentToken("C7dEdq9Mcz4nwyy")
    #     #card_obj.cvv("123")
    #     verify_obj.card(card_obj)
    #
    #     #shipping_obj.carrier("FEX")
    #     #shipping_obj.shipMethod("C")
    #     #shipping_obj.street("100 Queen Street West")
    #     #shipping_obj.city("Toronto")
    #     #shipping_obj.state("ON")
    #     #shipping_obj.country("CA")
    #     #shipping_obj.zip("M5H 2N2")
    #     #verify_obj.shippingDetails(shipping_obj)
    #
    #     #card_exp_obj.month("09")
    #     #card_exp_obj.year("2019")
    #     #card_obj.cardExpiry(card_exp_obj)
    #
    #     #billing_obj.street("100 Queen Street West")
    #     #billing_obj.city("Toronto")
    #     #billing_obj.state("ON")
    #     #billing_obj.country("CA")
    #     #billing_obj.zip("M5H 2N2")
    #     #verify_obj.billingDetails(billing_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).verify_card(verify_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    # def lookup_verification_using_id(self):
    #     '''
    #     dd655ad9-2ebe-4178-9b3f-c88707a193f3
    #     '''
    #     verify_obj = Verification(None)
    #     verify_obj.id("dd655ad9-2ebe-4178-9b3f-c88707a193f3")
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).lookup_verification_using_id(verify_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)
    #
    # def lookup_verification_using_merchant_ref_num(self):
    #     '''
    #     4lnvozq01d1pbkr0
    #     '''
    #     pagination_obj = Pagination(None)
    #     pagination_obj.limit = "4"
    #     pagination_obj.offset = "0"
    #     #pagination_obj.startDate = "2015-02-10T06:08:56Z"
    #     #pagination_obj.endDate = "2015-02-20T06:08:56Z"
    #
    #     verify_obj = Verification(None)
    #     verify_obj.merchantRefNum("4lnvozq01d1pbkr0")
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).lookup_verification_using_merchant_ref_num(verify_obj, pagination_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object)
    #     #print (response_object.links[0].rel)
    #     #print (response_object.links[0].href)
    #     #print (response_object[0].links[0].href)
    #     print (response_object[0].__dict__)
    #     #print (response_object.error.fieldErrors[0].__dict__)
    #     #print (response_object.error.fieldErrors[1].__dict__)
    #
    #     for c in range(0, response_object.__len__()):
    #         print ('Records : ', c)
    #         print ('Verifications : ', response_object[c].__dict__)
    #
    #
    # def create_transaction_test(self):
    #     '''
    #     Sample of complete transaction request
    #     '''
    #     billing_obj = BillingDetails(None)
    #     shipping_obj = ShippingDetails(None)
    #     auth_obj = Authorization(None)
    #     card_obj = Card(None)
    #     card_exp_obj = CardExpiry(None)
    #
    #     billing_obj.street("Carlos Pellegrini 551")
    #     billing_obj.city("Buenos Aires")
    #     billing_obj.state("CA")
    #     billing_obj.country("US")
    #     billing_obj.zip("M5H 2N2")
    #
    #     shipping_obj.carrier("CAD")
    #     shipping_obj.city("Buenos Aires")
    #     shipping_obj.state("ON")
    #     shipping_obj.country("CA")
    #     shipping_obj.zip("M5H 2N2")
    #
    #     card_obj.cardNum("5191330000004415")
    #     card_exp_obj.month("09")
    #     card_exp_obj.year("2019")
    #     card_obj.cardExpiry(card_exp_obj)
    #
    #     auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
    #     auth_obj.amount("1200")
    #     auth_obj.settleWithAuth(True)
    #     auth_obj.dupCheck(True)
    #     auth_obj.card(card_obj)
    #     auth_obj.billingDetails(billing_obj)
    #     auth_obj.shippingDetails(shipping_obj)
    #
    #     self._optimal_obj = OptimalApiClient(self._api_key,
    #                                          self._api_password,
    #                                          "TEST",
    #                                          self._account_number)
    #     response_object = self._optimal_obj.card_payments_service_handler(
    #                                         ).create_authorization(auth_obj)
    #
    #     print ("Complete Response : ")
    #     print (response_object.__dict__)


# Call Object
#o = SampleTest_Card().lookup_verification_using_merchant_ref_num()
cardp = CardPurchase()