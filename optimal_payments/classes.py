#
# optimal_payments/classes.py

from django.conf import settings
from datetime import datetime, date, timedelta
from django.utils import timezone
from django.db.transaction import atomic    # for transactions

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

from .models import Profile, Address
import optimal_payments.models

import random
import string
import inspect
import requests
import json
import base64

#
# source: https://developer.optimalpayments.com/en/sdk/server-side/python/card-payments-api/

class RandomTokenGenerator(object):
    """

    """
    def __init__(self):
        """
        """

        pass

    def generateToken(self):
        """

        """
        token = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(16))
        return (token)

class NetBanxApi(object):

    # for general exceptions in the api
    class NetBanxApiException(Exception): pass              # last resort error from unkonwn API error

    # specific error codes result in these exceptions:
    ERROR_CODE_7503 = '7503'
    ERROR_CODE_7505 = '7505'
    ERROR_CODE_7508 = '7508'
    ERROR_CODE_7511 = '7511'
    class CustomerCardExistsException(Exception): pass      # 7503 - card is already on the profile
    class CustomerIdExistsException(Exception): pass        # 7505 - a profile with this customer id already exists
    class InvalidCardNumOrBrand(Exception): pass            # 7508 - wrong cc number or brand or combo
    class AddressDoesNotExist(Exception): pass              # 7511 - address not found by its id

    # Static data
    _environment    = settings.OPTIMAL_ENVIRONMENT      # 'TEST' or 'LIVE'
    _api_key        = settings.OPTIMAL_API_KEY          # 'devcentre4628'
    _api_password   = settings.OPTIMAL_API_PASSWORD     # 'B-qa2-0-548ef25d-302b0213119f70d83213f828bc442dfd0af3280a7b48b1021400972746f9abe438554699c8fa3617063ca4c69a'
    _account_number = settings.OPTIMAL_ACCOUNT_NUMBER   # '89983472'

    def __init__(self):
        self.session = requests.Session()
        self.headers        = self.generate_base64_basic_auth_header(self._api_key, self._api_password)
        # also specify the content-type
        self.headers['Content-Type'] = 'application/json'

        self.user           = None # child classes MUSt set this
        self.model_class    = None # child classes MUST set this
        self.model_instance = None # child classes should set this in save_model() on successful save

    def save_model(self, response_json):
        """
        create but do not save an instance of the internal model_class.

        child classes should call this method to get a new unsaved
        model instance with the user, and oid set

        :param response_json:
        :return:
        """
        if self.model_class is None:
            raise Exception('self.model_class was never set (its None!)')

        instance = self.model_class()

        if self.user is None:
            raise Exception('self.user was never set (its None!)')
        instance.user   = self.user

        oid = response_json.get('id')
        if oid is None:
            raise Exception('oid was not set in super().save_model()!')

        instance.oid = oid
        return instance

    def generate_base64_basic_auth_header(self, key, password):
        """
        base64 encode the api_key and return it formatted for the http request header
        """
        api_key = '%s:%s' % (key, password)
        utf8 = 'utf8'
        return { 'Authorization' : 'Basic %s' % base64.b64encode(api_key.encode(utf8)).decode(utf8) }

    def handle_error(self, error_obj):
        """
        if error_obj is None - then no checking is done, and the method returns immediately

        display and deal with whatever the error is.

        each error will have a code and a link to the error,
        and a message

        example error object:

            {   'code': '7505',
                 'links': [
                    {   'rel': 'errorinfo',
                        'href': 'https://developer.optimalpayments.com/en/documentation/customer-vault-api/error-7505'
                    }, # there could be more than 1 object seems like
                ],
                'message': 'The merchantCustomerId provided for this profile has already been used for another profile - 94649a20-5da7-4c34-b8e2-3d6c7ea4c092'}
            }

        :param error:
        :return:
        """
        if error_obj is None:
            return # there is no error

        code    = error_obj.get('code')
        links   = error_obj.get('links', [])  # the error link
        message = error_obj.get('message')

        if code == self.ERROR_CODE_7503:
            raise self.CustomerCardExistsException( str(message) )
        elif code == self.ERROR_CODE_7505:
            raise self.CustomerIdExistsException( str(message) )
        elif code == self.ERROR_CODE_7508:
            raise self.InvalidCardNumOrBrand( str(message) )
        elif code == self.ERROR_CODE_7511:
            raise self.AddressDoesNotExist( str(message) )
        elif code is not None:
            print( str(links) )
            raise self.NetBanxApiException( str(message) )

    def check_errors(self, json_str):
        """
        convert a string (from the body of an http response) to json.

        check for errors, and then if there are none return the json response
        """
        try:
            response_json = json.loads( json_str )
        except:
            e = 'could not convert response text to json object!'
            print( e )
            raise Exception( e )

        # check if there is an error first
        err = response_json.get('error')
        # handle the error if there is one - this may raise exceptions
        self.handle_error( err )

        #
        return response_json

class CustomerProfile( NetBanxApi ):

    def __init__(self):
        super().__init__()
        self.model_class    = Profile
        # self.model_instance = None
        self.url_create     = 'https://api.test.netbanx.com/customervault/v1/profiles'
        self.r              = None # the response from the api

    def get_or_create(self, user):
        """
        Returns a tuple in the same form as models get_or_create() method.
        ie: it will return: (object, boolean) and the boolean indicates
        if the object was just created or not.

        if it cant be gotten because it doesnt exist, create it and return it.

        calls the create() method in the case it must be created.

        :param user:
        :return:
        """
        newly_created = False
        try:
            profile = self.model_class.objects.get( user=user )
        except self.model_class.DoesNotExist:
            profile = self.create( user )
            newly_created = True

        return profile, newly_created

    def create(self, user):
        """
        Create a Customer Profile via the api and create a models.Profile entry

        returns the created profile instance
        """

        self.user = user    # set the user before the model instance is created

        # payment_email = user.email
        # if email is not None: payment_email = email

        params = {
            "merchantCustomerId"    : str(user.pk),
            "locale"                : "en_US",
            "firstName"             : user.first_name,
            "lastName"              : user.last_name,
            "phone"                 : '',
            "email"                 : user.email
        }
        self.r = self.session.post( self.url_create, headers=self.headers, data=json.dumps( params ) )

        # get response json, and check for errors
        response_json = self.validate_response( self.r )

        # save the customers profile to the database on success
        self.model_instance = self.save_model( response_json )
        return self.model_instance

    def save_model(self, response_json):
        """
        save the profile to the database
        """

        # parent save_model() gets an instance with the user, and oid set
        p = super().save_model( response_json )

        p.status              = response_json.get('status')               # unused, however
        p.merchant_customer   = response_json.get('merchantCustomerId')
        p.first_name          = response_json.get('firstName')
        p.last_name           = response_json.get('lastName')
        p.phone               = response_json.get('phone')              # form: "111-111-1117"
        p.email               = response_json.get('email')
        p.payment_token       = response_json.get('paymentToken')
        p.save()              # commit to db
        return p

    def validate_response(self, r):
        """
        check for errors
        """
        print( r.text )

        # error-5279 - the authentication credentials are invalid
        # {"error": {"code": "5279","message": "The authentication credentials are invalid.",
        #   "links": [{"rel": "errorinfo","href": "https://developer.optimalpayments.com/en/documentation/customer-vault-api/error-5279"}]}}

        # error-5023 - the request is not parseable
        # {"error":{"code":"5023","message":"Cannot process request",
        #   "links":[{"rel":"errorinfo","href":"https://developer.optimalpayments.com/en/documentation/customer-vault-api/error-5023"}]}}

        # if it already exists:
        # {"error":{"code":"7505",
        #   "message":"The merchantCustomerId provided for this profile has already been used for another profile - 94649a20-5da7-4c34-b8e2-3d6c7ea4c092",
        #   "links":[{"rel":"errorinfo","href":"https://developer.optimalpayments.com/en/documentation/customer-vault-api/error-7505"}]},"links":[{"rel":"existing_entity","href":"https://api.test.netbanx.com/customervault/v1/profiles/94649a20-5da7-4c34-b8e2-3d6c7ea4c092"}]}

        # success will look something like:
        # {"id":"9ec08740-24a3-48d7-8021-ff6817512165","status":"ACTIVE",
        #   "merchantCustomerId":"mycustomer1","locale":"en_US",
        #   "firstName":"John","lastName":"Smith","paymentToken":"Pg8M8PiG8606Bdf",
        #   "phone":"713-444-5555","email":"john.smith@somedomain.com"}

        response_json = self.check_errors( r.text )
        return response_json

class CreateAddress(NetBanxApi):

    def __init__(self, profile_instance):
        super().__init__()
        self.model_class        = Address
        # self.model_instance     = None
        self.user               = profile_instance.user
        self.profile_instance   = profile_instance

        self.url = 'https://api.test.netbanx.com/customervault/v1'

        self.url_create = self.url + '/profiles'
        self.url_create += '/%s/addresses' % self.profile_instance.oid

        self.url_delete = self.url + '/profiles'
        self.url_delete += '/%s/addresses/' % (profile_instance.oid)

        self.r                  = None # the response from the api

    def delete(self, oid):
        """
        remove an Address from a netbanx Profile

        url: /profiles/{PROFILE_ID}/addresses/{ADDRESS_ID}
        """

        # get the address object in our own database
        address = Address.objects.get( oid=oid )
        address_oid = address.oid

        # delete the address from optimal with the api
        self.r = self.session.delete( self.url_delete + address_oid, headers=self.headers )

    def create(self, nickname, street, city, state, zip, country='US'):
        """
        create an Address to associate with a  Customer Profile via the api.

        this method returns the newly created Address on successful creation
        """
        params = {
            "nickname"      : nickname,
            "street"        : street,
            "city"          : city,
            "state"         : state,
            "country"       : country,
            "zip"           : zip
        }
        self.r = self.session.post( self.url_create, headers=self.headers, data=json.dumps( params ) )

        # get response json, and check for errors
        response_json = self.validate_response( self.r )

        # save the Address for the customer profile
        self.model_instance = self.save_model( response_json )
        return self.model_instance

    def save_model(self, response_json):
        """
        save this Adddress for the Profile

        a successful response example:

            {
                "id":"28df601f-934e-4590-a1a0-0947eb4eb0c2",
                "street":"1 Some Street","city":"Sometown","country":"US",
                "state":"NH","zip":"03055",
                "defaultShippingAddressIndicator":false,"status":"ACTIVE"
            }

        """

        # parent save_model() gets an instance with the user, and oid set
        address = super().save_model( response_json )

        address.street      = response_json.get('street')
        address.city        = response_json.get('city')
        address.state       = response_json.get('state')
        address.country     = response_json.get('country')
        address.zip         = response_json.get('zip')
        address.default     = response_json.get('defaultShippingAddressIndicator')  # boolean
        address.save()      # commit it to db
        return address

    def validate_response(self, r):
        """
        check for errors, and get the json from the response
        """
        print( r.text )
        response_json = self.check_errors( r.text )
        return response_json

class CreateCard(NetBanxApi):

    def __init__(self, profile_instance, address_instance):
        super().__init__()
        self.model_class        = optimal_payments.models.Card
        self.profile_instance   = profile_instance
        self.user               = address_instance.user
        self.address_instance   = address_instance

        self.url = 'https://api.test.netbanx.com/customervault/v1'
        self.url_create = self.url + '/profiles'
        self.url_create += '/%s/cards' % profile_instance.oid

        self.url_delete = self.url + '/profiles'
        self.url_delete += '/%s/cards/' % (profile_instance.oid)

        self.r                  = None # the response from the api

    def delete(self, oid):
        """
        remove a card from a netbanx profile

        url: /profiles/{PROFILE_ID}/cards/{CARD_ID}
        """

        # get the Card model
        c = self.model_class.objects.get(oid=oid)
        address_oid = c.address_oid

        # delete this card from the profile
        self.r = self.session.delete( self.url_delete + c.oid, headers=self.headers )

    def create(self, nickname, holder_name, cc_num, exp_month, exp_year):
        """
        create an Address to associate with a  Customer Profile via the api.

        returns the newly created Card instance if successfully created
        """
        params = {
            "billingAddressId"  : self.address_instance.oid,
            "nickName"          : nickname,
            "holderName"        : holder_name,
            "cardNum"           : cc_num,
            "cardExpiry"        : { 'month' : exp_month, 'year' : exp_year },
        }
        print('CreateCard params:')
        print( str(params) )
        self.r = self.session.post( self.url_create, headers=self.headers, data=json.dumps( params ) )

        response_json = self.validate_response( self.r )
        self.model_instance = self.save_model( response_json )
        return self.model_instance

    def save_model(self, response_json):
        """
        create the Card which is associated with an Address.

        returns the newly created model instance.

        here is an example of what the response_json looks like on success:

            {
                "status":"ACTIVE","id":"b3505d3e-dd30-4785-bbf8-39bc5e65faf1",
                "cardBin":"453091","lastDigits":"2345",
                "cardExpiry":{"year":2017,"month":11},
                "holderName":"Holder Name","nickName":"nicknameOfCard",
                "billingAddressId":"31847648-9401-48c7-b9ec-3515e19c50d1",
                "cardType":"VI","paymentToken":"CTPvTXm3IrLGMgy",
                "defaultCardIndicator":true
            }

        """

        # parent save_model() gets an instance with the user, and oid set
        card = super().save_model( response_json )

        card.address_oid    = response_json.get('billingAddressId')
        card.holder_name    = response_json.get('holderName')
        card.last_digits    = response_json.get('lastDigits')
        card.card_type      = response_json.get('cardType')
        card.payment_token  = response_json.get('paymentToken')
        card.save()     # commit to db
        return card

    def validate_response(self, r):
        """
        check for errors
        """
        print( r.text )
        response_json = self.check_errors( r.text )
        return response_json

class PaymentMethodManager(object):
    """
    This class is a wrapper for the CustomerProfile, CreateAddress, and CreateCard classes
    to make it easier to add and remove payment methods.

    Note: Many of the methods in this class make use of an external api
    and take tangible time to complete (a few seconds at most).

    a User has a single CustomerProfile object. This is created with the
    netbanx api and exists on their servers, but we hold a record for it
    in our own database using CustomerProfile.

    A "Payment Method" is represented thru this class as a single entity,
    because we are abstracting the fact that we create a brand new address
    for every card we add. (And we delete that address when we delete a Card.)

    This abstraction is possible because we can create multiple identical
    Address objects associated with the Customer Profile via the netbanx api
    and it simplifies things on our end to group them together.
    """

    def __init__(self, user):
        self.user = user

    def get_profile(self):
        """
        create a profile using the CustomerProfile object
        """
        cp = CustomerProfile()
        profile, created = cp.get_or_create(self.user)
        return profile

    def get_payment_methods(self):
        """
        returns a list of the user's Card objects
        """
        return optimal_payments.models.Card.objects.filter(user=self.user)

    @atomic
    def create(self, billing_nickname, street, city, country, zip,
                     card_nickname, holder_name, card_num, exp_month, exp_year):
        """
        Create a new payment method by a) creating a new Address
        and b) by creating a new Card object.

        This is an atomic method.

        TODO - exception handling?
        """

        address_manager = CreateAddress( self.get_profile() )
        address_instance = address_manager.create(billing_nickname, street, city, country, zip)

        card_manager = CreateCard( self.get_profile(), address_instance )
        card_instance = card_manager.create(card_nickname, holder_name, card_num, exp_month, exp_year)

    @atomic
    def delete(self, card_oid):
        """
        Delete a payment method by deleting the Card, as well as the Address.

        This is an atomic method.
        """

        profile_instance = self.get_profile()

        #
        # we need to get the Card entry first, so we also know the Address oid
        card_instance       = Card.objects.get(oid=card_oid)
        address_oid         = card_instance.address_oid
        address_instance    = Address.objects.get(oid=address_oid)

        #
        # use the address manager to remove the Card
        # from netbanx, as well as in our own database
        card_manager    = CreateCard( profile_instance, address_instance )
        card_manager.delete(card_oid)           # delete from netxbanx server
        card_instance.delete()                  # delete model

        #
        # now we can remove the Address from netbanx
        # and from our own datbase
        address_manager = CreateAddress( profile_instance )
        address_manager.delete(address_oid)     # delete from netbanx server
        address_instance.delete()               # delete model

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
    COMPLETED       = 'COMPLETED'
    MONITOR_READY   = 'READY'

    #
    # error codes in the various ranges will raise different exceptions.
    # consolidating the exceptions will be useful because
    # we really dont care about the majority of the specific error cases.
    PROCESSING_EXCEPTION_ERROR_RANGE    = range(0,      1999+1)  # 0     - 1999
    PAYMENT_DECLINED_ERROR_RANGE        = range(2000,   4999+1) # 2000  - 4999

    # Static data
    _environment    = settings.OPTIMAL_ENVIRONMENT      # 'TEST' or 'LIVE'
    _api_key        = settings.OPTIMAL_API_KEY          # 'devcentre4628'
    _api_password   = settings.OPTIMAL_API_PASSWORD     # 'B-qa2-0-548ef25d-302b0213119f70d83213f828bc442dfd0af3280a7b48b1021400972746f9abe438554699c8fa3617063ca4c69a'
    _account_number = settings.OPTIMAL_ACCOUNT_NUMBER   # '89983472'

    #
    #################################################################
    # exceptions - class related exception
    #################################################################

    # the api service is not currently accessible
    class OptimalServiceMonitorDownException(Exception): pass

    # the monitor is not responding with "READY" status
    class OptimalServiceMonitorNotReadyException(Exception): pass

    # raised when a function argument is invalid for whatever reason
    class InvalidArgumentException(Exception): pass

    # if the exp_month and exp_year are expired
    class ExpiredCreditCardException(Exception): pass

    #
    #################################################################
    # exceptions - response related errors from the card payment api
    #################################################################

    # error codes: < 2999  (timeouts, internal errors w/ proccessor)
    class ProcessingException(Exception): pass

    # error codes >= 3000: 3009, 3015, 3022, 3023, 3024, etc...
    class PaymentDeclinedException(Exception): pass

    # used for error codes outside of the range, as
    # well as other exception cases we dont have a
    # good reason for, but which happened because of the api
    class UnknownNetbanxErrorCodeException(Exception): pass

    # raise when we get a response from the api for
    # processing a payment, but the status does not indicate success
    class ProcessPaymentResponseStatusException(Exception): pass

    def __init__(self):
        '''
        Constructor
        '''
        #print('OptimalPayments: %s' % settings.OPTIMAL_ENVIRONMENT)

        self.optimal_obj        = None
        self.r_process_payment  = None   # the last process_payment() response

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

    def __validate_credit_card_expiration_month_and_year(self, exp_month, exp_year):
        """

        :param exp_month:
        :param exp_year:
        :return:
        """
        if exp_month is None:
            raise self.InvalidArgumentException('exp_month cant be None')
        if exp_year is None:
            raise self.InvalidArgumentException('exp_year cant be None')

        try:
            exp_month = int( exp_month )
        except:
            raise self.InvalidArgumentException('exp_month [%s] must be an integer value!' % str(exp_month))

        try:
            exp_year = int( exp_year )
        except:
            raise self.InvalidArgumentException('exp_year [%s] must be an integer value!' % str(exp_year))

        # make sure its withing the range, but not against current date yet
        if exp_month not in range(1,12+1):
            # the month is not in the range 1 to 12
            raise self.InvalidArgumentException('exp_month [%s]' % str(exp_month))

        # check potential ranges, but not against current date yet
        if exp_year <= 2000:
            raise self.InvalidArgumentException('exp_year [%s] - must be greater than 2000' % str(exp_year))

        now = timezone.now()
        now_date = now.date()
        expiration_date = date( exp_year, exp_month, 1 )

        if expiration_date <= now_date:
            msg_fmt = 'expiration date: %s/%s'
            raise self.ExpiredCreditCardException( msg_fmt % (str(exp_month), str(exp_year)))

        return str(exp_month), str(exp_year)

    def __validate_credit_card_cvv(self, cvv):
        """

        :param cvv:
        :return:
        """
        if cvv is None:
            raise self.InvalidArgumentException('cvv [%s]' % str(cvv))

        try:
            cvv = int(cvv)
        except:
            raise self.InvalidArgumentException('cvv [%s] must contain an integer value' % str(cvv))

        return str(cvv) # back to string, because that is what the api requires

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
            raise self.InvalidArgumentException('the zipcode must contain 5 characters: %s' % billing_zipcode)

        try:
            billing_zipcode = int(billing_zipcode)
        except ValueError:
            raise self.InvalidArgumentException('the zipcode must only contain numerical characters: %s' % billing_zipcode)

        billing_zipcode = str(billing_zipcode).zfill(self.BILLING_ZIPCODE_LENGTH)

        return billing_zipcode

    def process_purchase_token(self, amt, payment_token, settleWithAuth=True):
        """

        :param amt:
        :param settleWithAuth:
        :return:
        """
        amt_hundreds        = self.__validate_amount( amt )

        #
        # ensure the payemnts api is ready by checking status of the card payments monitor
        self.card_payments_monitor()

        #
        # build the card purchase
        auth_obj = Authorization(None)
        card_obj = Card(None)
        auth_obj.merchantRefNum(RandomTokenGenerator().generateToken())
        auth_obj.amount(str(amt_hundreds))
        auth_obj.settleWithAuth("true" if settleWithAuth else "false")
        card_obj.paymentToken( payment_token )
        auth_obj.card( card_obj )

        # call the api to swipe the credit card!
        self.r_process_payment = self.optimal_obj.card_payments_service_handler().create_authorization(auth_obj)

        # check the response -- will raise errors if they exist
        self.__validate_payment( self.r_process_payment )
        return self.r_process_payment.__dict__.get('id')

    def process_purchase(self, amt, cc_num, cvv,
                                      exp_month, exp_year,
                                      billing_zipcode,
                                      settleWithAuth=True):
        """
        process the purchase amount with the given credit card information.

        the 'amt' specified should be the intuitive amount, ie: 55.34,
        although internally this method will multiply by 100 and truncate remaining decimal places!

        Note on 'settleWithAuth':

           "... by setting the flag settleWithAuth to true, the card processing
           system will automatically charge the card as part of the same request.
           If you are shipping physical items, you should not perform the
           settlement until the items are actually shipped."

           src: https://developer.optimalpayments.com/en/documentation/card-payments-api/process-a-purchase/

        The response for sucessfully processing a purchase:

           "The status is set to COMPLETED and the value for availableToSettle is 0
            because the card was automatically charged as part of the request,
            since the settleWithAuth flag was set to true. You may look up the
            transaction at any future time using either the
            merchantRefNum (demo-1) or the id (ebf6ae3d-88e1-40da-9b98-81044467345b)."

            src: https://developer.optimalpayments.com/en/documentation/card-payments-api/purchase-response/

        :param amt:
        :param cc_num:
        :param cvv:
        :param exp_month:
        :param exp_year:
        :param billing_zipcode:
        :param settleWithAuth:
        :return:
        """
        # validate the arguments passed in here for type, and size validity,
        # but let the API do the rest of the work.
        amt_hundreds        = self.__validate_amount( amt )
        cc_num              = self.__validate_credit_card_number( cc_num )
        exp_month, exp_year = self.__validate_credit_card_expiration_month_and_year( exp_month, exp_year )
        cvv                 = self.__validate_credit_card_cvv( cvv )
        billing_zipcode     = self.__validate_zipcode( billing_zipcode )

        #return None

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

        # call the api to swipe the credit card!
        self.r_process_payment = self.optimal_obj.card_payments_service_handler().create_authorization(auth_obj)

        # check the response -- will raise errors if they exist
        self.__validate_payment( self.r_process_payment )
        return self.r_process_payment.__dict__.get('id')

    def __validate_payment(self, response):
        """
        inspect the API response of a credit card payment.

        exceptions will be raised if errors or  status codes are found which
        do not indicate a successful payment has been processed.

        :param response:
        :return:
        """

        #
        # for reasons that escape me, the designers
        # of the netbanx api use method names
        # that they want to be property names,
        # so if response.error is of type 'method' then it hasnt
        # had an instance of Error() set to it (ie: there is no error)
        #
        # if its NOT a method, then there is an error object instance instead
        if not inspect.ismethod( response.error ):
            #
            # there is an error.
            # check on the error range, and raise the appropriate exception
            ecode       = int(response.error.code)
            err_msg     = 'netbanx error: %s' % ecode
            if ecode in self.PROCESSING_EXCEPTION_ERROR_RANGE:
                raise self.ProcessingException(err_msg)

            elif ecode in self.PAYMENT_DECLINED_ERROR_RANGE:
                raise self.PaymentDeclinedException(err_msg)

            else:
                raise self.UnknownNetbanxErrorCodeException(err_msg)

        #
        # also make sure the status matches the processed payment status expected
        if response.status and response.status != self.COMPLETED:
            raise self.ProcessPaymentResponseStatusException(str(response.status))

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

    def lookup_authorization_with_id(self):
        '''
        Lookup Authorization with Id
        '''

        # get the authorization id from the response of the process_payment method
        authorization_id = self.r_process_payment.__dict__.get('id')

        auth_obj = Authorization(None)
        #auth_obj.id("5406f84a-c728-499e-b310-c55f4e52af9f")
        auth_obj.id( authorization_id )

        self.optimal_obj = OptimalApiClient(self._api_key,
                                             self._api_password,
                                             self._environment,
                                             self._account_number)

        self.r_lookup_auth_with_id = self.optimal_obj.card_payments_service_handler(
                                            ).lookup_authorization_with_id(auth_obj)
        print ("lookup_authorization_with_id response: ")
        print (self.r_lookup_auth_with_id.__dict__)

cardp = CardPurchase()