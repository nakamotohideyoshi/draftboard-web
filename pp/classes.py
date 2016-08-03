#
# classes.py

from django.conf import settings
import requests
import json
from util.timesince import timeit
import paypalrestsdk as paypal
from rest_framework.exceptions import (
    APIException,
)
import pp.serializers
from pp.models import (
    SavedCardPaymentData,
    CreditCardPaymentData
)
import braintree
import cash


class VZeroShipping(object):

    class ValidationError(Exception):
        pass

    field_first_name = "first_name"
    field_last_name = "last_name"
    # field_company               = "company"
    field_street_address = "street_address"
    field_extended_address = "extended_address"
    field_locality = "locality"            # for US: this is the city, ie: "Austin"
    field_region = "region"              # for US: this is the state code, ie: "TX"
    field_postal_code = "postal_code"         # for US: this is the zipcode, ie: "12345"
    field_country_code_alpha2 = "country_code_alpha2"

    valid_fields = [
        field_first_name,
        field_last_name,
        # field_company,
        field_street_address,
        field_extended_address,
        field_locality,
        field_region,
        field_postal_code,
        field_country_code_alpha2,
    ]

    def __init__(self, data=None):
        self.data = data
        if self.data is None:
            self.data = {
                "first_name":           None,           # "Jen",
                "last_name":            None,           # "Smith",
                # "company":              "",             # "ABC Co.",
                "street_address":       None,           # "1 E 1st St",
                "extended_address":     "",             # "Suite 403",
                "locality":             None,           # "Bartlett",
                "region":               None,           # "IL",
                "postal_code":          None,           # "60103",
                "country_code_alpha2":  None,           # "US"
            }

    def validate(self):
        """
        validates the internal data

        raises any validation exceptions if they exist.
        """
        for field in self.valid_fields:
            if self.data.get(field) is None:
                raise self.ValidationError("'%s' must be set." % field)

    def update_field(self, field, val):
        if not isinstance(val, str):
            raise Exception('param "val" should be a string!')
        self.data[field] = val

    # def update_shipping_information(self, first_name, last_name, company,
    #                                         street_address, extended_address,
    #                                         locality, region, postal_code, country_code_alpha2):
    #     """ update the shipping address by setting each field manually """
    #     pass

    def update_data(self, data):
        self.data = data
        self.validate()

    def from_serializer(self, vzero_shipping_serializer):
        vzero_shipping_serializer.is_valid(raise_exception=True)
        self.update_data(vzero_shipping_serializer.data)


class VZeroTransaction(object):

    class ValidationError(Exception):
        pass

    default_customer_cc_statement_description = "drftbrd*deposit"
    default_paypal_email_receipt = "draftboard.com deposit"

    default_currency = "USD"
    choices_currency = [default_currency]  # we may add CAD (canadien) eventually...

    field_amount = "amount"
    field_currency = "merchant_account_id"     # strange name, but here we set the currency
    field_payment_method_nonce = "payment_method_nonce"
    field_shipping = "shipping"

    valid_fields = [
        field_amount,
        field_currency,
        field_payment_method_nonce

        # purposely excludes 'shipping' because its a dict and should validate itself
    ]

    def __init__(self):
        # construct the data with some None values internally.
        # we will perform validation on it before being used.
        self.data = {

            "amount": None,                                        # TODO - this will need to be set
            "merchant_account_id": self.default_currency,           # defaults to "USD"
            "payment_method_nonce": None,                          # TODO - will need to set
            "order_id": "Mapped to PayPal Invoice Number",
            "descriptor": {
                #
                # Descriptor displayed in customer CC statements. [22 char max]
                "name": self.default_customer_cc_statement_description
            },

            "shipping": None,                                       # TODO - validate its been set

            "options": {
                "paypal": {
                    "custom_field": "PayPal custom field",
                    #
                    # "Description for PayPal email receipt"
                    "description": self.default_paypal_email_receipt,
                },
            }
        }

    def validate(self):
        """
        raises an exception if a required field has not been set.
        """
        for field in self.valid_fields:
            if self.data.get(field) is None:
                raise self.ValidationError("'%s' field must be set." % field)

    def update_field(self, field, val):
        self.data[field] = val

    def update_shipping_data(self, data):
        # update the shipping data
        self.update_field(self.field_shipping, data)

    def update_transaction_data(self, data):
        self.update_field(self.field_amount, data.get(self.field_amount))
        self.update_field(self.field_payment_method_nonce,
                          data.get(self.field_payment_method_nonce))

    def update_data(self, shipping_data, transaction_data):
        """

        """

        # update the shipping data
        self.update_shipping_data(shipping_data)

        # update the transaction data (amount, currency, nonce...)
        self.update_transaction_data(transaction_data)

        # raise exceptions if any required fields are not set
        self.validate()


class VZero(object):

    class VZeroException(Exception):
        pass

    access_token = settings.VZERO_ACCESS_TOKEN

    def __init__(self, access_token=None):  # add user param ?
        # django user who is performing a transaction
        # self.user = user

        # override the access_token if its specified
        if access_token is not None:
            self.access_token = access_token

        # setup the gateway which will help us do braintree/vzero things
        self.gateway = braintree.BraintreeGateway(access_token=self.access_token)

    def get_client_token(self):
        """
        the client requires our server to provide this token so they
        can do client stuff and build a payment_method_nonce which
        will be given back to the server at the point they wish
        to make a transaction.

        :return: client_token
        """
        client_token = self.gateway.client_token.generate()
        return client_token

    # test this if we are going to use it
    # def create_transaction_from_serializer(self, vzero_deposit_serializer):
    #     vzero_transaction = VZeroTransaction()
    #     vzero_transaction.from_serializer(vzero_deposit_serializer)
    #
    #     # create the transaction sale, and return the result
    #     return self.create_transaction(vzero_transaction)

    def create_transaction(self, vzero_transaction):
        """
        create the transaction using the vzero serializer for easy use
        """

        # use the gateway to make the sale (aka: the deposit)
        result = self.gateway.transaction.sale(
            vzero_transaction.data
        )

        #
        if not result.is_success:
            #
            # example of deep errors (a list)
            #   [<ValidationError {attribute: 'payment_method_nonce', message: 'Unknown or expired
            #   payment_method_nonce.', code: '91565'} at 140660839155080>]
            # TODO remove this debugging print eventually !
            print("braintree transaction | Failure deep errors: %s" %
                  str(result.errors.deep_errors))
            for e in result.errors.deep_errors:
                raise self.VZeroException(e.message)

        #
        # success
        # TODO remove this debugging print eventually !
        print("braintree transaction | Success ID: %s" % str(result.transaction.id))
        return result.transaction.id

# these 4 un-classed methods are for testing. they come from wikipedia
#    source: https://en.wikipedia.org/wiki/Luhn_algorithm
# and they can help us create testing credit card numbers


def digits_of(number):
    return list(map(int, str(number)))


def luhn_checksum(card_number):
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(digits_of(2 * digit))
    return total % 10


def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0


def calculate_luhn(partial_card_number):
    # Append a zero check digit to the partial number and calculate checksum
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    # If the (sum mod 10) == 0, then the check digit is 0
    return check_digit if check_digit == 0 else 10 - check_digit
    # Else, the check digit = 10 - (sum mod 10)


class CardData(object):
    # card = {
    #     "payer_id":external_user_id,
    #     "external_customer_id":external_user_id,
    #     "type":"visa",
    #     "number":"4417119669820331",
    #     "expire_month":"11",
    #     "expire_year":"2018",
    #     "first_name":"Betsy",
    #     "last_name":"Buyer",
    #     "billing_address":{
    #         "line1":"111 First Street",
    #         "city":"Saratoga",
    #         "country_code":"US",
    #         "state":"CA",
    #         "postal_code":"95070"
    #     }
    # }

    class InvalidCardFieldException(Exception):
        pass

    class InvalidBillingFieldException(Exception):
        pass

    BILLING_ADDRESS_DATA = 'billing_address'

    # will get set when external_customer_id set
    PAYER_ID = 'payer_id'

    EXTERNAL_CUSTOMER_ID = 'external_customer_id'        # string
    TYPE = 'type'                        # card type, ie: 'visa'
    NUMBER = 'number'                      # credit card number, ie: "4417119669820331" (string)
    EXPIRE_MONTH = 'expire_month'                # exp month (string)
    EXPIRE_YEAR = 'expire_year'                 # exp year (string)
    CVV2 = 'cvv2'                        # cvv2 code
    FIRST_NAME = 'first_name'
    LAST_NAME = 'last_name'

    # used for validation
    CARD_FIELDS = [
        EXTERNAL_CUSTOMER_ID, TYPE, NUMBER, EXPIRE_MONTH, EXPIRE_YEAR, FIRST_NAME, LAST_NAME, CVV2
    ]

    # billing address information
    LINE_1 = 'line1'                       # first line of address
    CITY = 'city'                        # ie: 'Saratoga' (string)
    COUNTRY_CODE = 'country_code'                # ie: 'US'
    STATE = 'state'                       # ie: 'CA'
    POSTAL_CODE = 'postal_code'                 # ie: '95070' (string)

    # used for validation
    BILLING_FIELDS = [
        LINE_1, CITY, COUNTRY_CODE, STATE, POSTAL_CODE
    ]

    def __init__(self, data=None):
        self.data = data
        if self.data is None:
            self.data = {
                self.PAYER_ID: None,
                self.EXTERNAL_CUSTOMER_ID: None,
                self.TYPE: None,
                self.NUMBER: None,
                self.EXPIRE_MONTH: None,
                self.EXPIRE_YEAR: None,
                self.CVV2: None,
                self.FIRST_NAME: None,
                self.LAST_NAME: None,
                self.BILLING_ADDRESS_DATA: {
                    self.LINE_1: None,
                    self.CITY: None,
                    self.COUNTRY_CODE: None,
                    self.STATE: None,
                    self.POSTAL_CODE: None,
                }
            }

    def get_data(self):
        return self.data

    def get_number(self):
        return self.data.get(self.NUMBER)

    def get_type(self):
        return self.data.get(self.TYPE)

    def get_exp_month(self):
        return self.data.get(self.EXPIRE_MONTH)

    def get_exp_year(self):
        return self.data.get(self.EXPIRE_YEAR)

    def get_cvv2(self):
        return self.data.get(self.CVV2)

    def get_first_name(self):
        return self.data.get(self.FIRST_NAME)

    def get_last_name(self):
        return self.data.get(self.LAST_NAME)

    def set_card_field(self, field, value):
        if field not in self.CARD_FIELDS:
            raise self.InvalidCardFieldException(field)
        self.data[field] = value
        # setting the external customer id also sets the payer id to make them identical!
        if field == self.EXTERNAL_CUSTOMER_ID:
            self.data[self.PAYER_ID] = value

    def set_billing_field(self, field, value):
        if field not in self.BILLING_FIELDS:
            raise self.InvalidBillingFieldException(field)
        self.data[self.BILLING_ADDRESS_DATA][field] = value

# class SavedCard(object):
#
#     def __init__(self, data):
#         self.data = data


class PayPal(object):
    #
    # apparently this is possible:
    # HTTP [503] Service Unavailable
    # BODY
    # [{"name":"INTERNAL_SERVICE_ERROR","information_link":"https://api.sandbox.paypal.com/docs/api/#INTERNAL_SERVICE_ERROR","debug_id":"1635acf4b1f6c"}]

    # this can also happen during payments:
    # In [9]: r = p.pay_with_credit_card(25, 'mastercard', '5500005555555559', 12, 2018, 111, 'Betsy', 'Buyer')
    # headers: {'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'python-requests/2.6.0 CPython/3.4.3 Linux/3.13.0-49-generic', 'Accept': '*/*', 'Connection': 'keep-alive'}
    # cookies: <RequestsCookieJar[<Cookie X-PP-SILOVER=name%3DSANDBOX3.API.1%26silo_version%3D1880%26app%3Dplatformapiserv%26TIME%3D3092539479%26HTTP_X_PP_AZ_LOCATOR%3D for .paypal.com/>]>
    # HTTP [400] Bad Request
    # BODY [{"name":"UNKNOWN_ERROR","message":"An unknown error has
    # occurred","information_link":"https://developer.paypal.com/webapps/developer/docs/api/#UNKNOWN_ERROR","debug_id":"ce216adf53370"}]

    class UnimplementedMethodException(Exception):
        pass

    class AuthException(Exception):
        pass

    class PayPalException(Exception):
        pass

    class PayWithCreditCardException(Exception):
        pass

    class PayWithSavedCardException(Exception):
        pass

    class InvalidSavedCardIdException(Exception):
        pass

    # TODO add pay wtih paypal account exception

    api = 'https://api.sandbox.paypal.com'  # 'https://api.paypal.com'

    api_vault = api + '/v1/vault'
    api_payments = api + '/v1/payments'
    api_oauth_token = api + '/v1/oauth2/token'

    def __init__(self):
        self.session = requests.Session()
        self.auth_data = None  # set when auth() has been called

        # response values for debugging - officially speaking, dont use outside of
        # the methods that set them
        self.r_login = None
        self.r_save_card = None
        self.r_delete_card = None
        self.r_show_card_details = None
        self.r_payment = None

    def get_headers(self):
        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Bearer %s' % self.get_access_token()}
        return headers

    def pay_with_paypal(self):
        """
        https://developer.paypal.com/docs/integration/web/accept-paypal-payment/
        """
        # TODO - this requires a bit more complicated flow between us and paypal
        raise self.UnimplementedMethodException('pay_with_paypal() - TODO')

    def get_formatted_amount(self, amount):
        """
        This method expects a float amount [sort of].

        However, if the amount is an integer or a string
        we attempt to format it into a float for ease of use.

        :param amount:
        :return:
        """
        # print('formatted_amount before [%.2f]' % amount)
        formatted_amount = amount
        print('formatted_amount before [%.2f]' % amount)
        # if isinstance(formatted_amount, str) or isinstance(formatted_amount, int):
        # attempt to cast to float() and format into 2 decimal place string
        formatted_amount = '%.2f' % float(formatted_amount)
        print('formatted_amount after [%s]' % formatted_amount)
        return formatted_amount

    def save_payment_data(self, model_class, payment_data):
        model = model_class()
        model.payment_data = payment_data
        model.save()

    def pay_with_saved_card(self, amount, external_customer_id, saved_card_id):
        # format the amount
        formatted_amount = self.get_formatted_amount(amount)
        payment_data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [
                    {
                        "credit_card_token": {
                            # ie: "CARD-1MD19612EW4364010KGFNJQI",
                            "credit_card_id": saved_card_id,
                            # ie: "ppuser12345",
                            "payer_id": external_customer_id
                        }
                    }
                ]
            },
            "transactions": [
                {
                    "amount": {
                        "total": formatted_amount,       # ie:"total": "7.47",
                        "currency": "USD"
                    },
                    "description": "This is the payment transaction description."
                }
            ]
        }

        # print('payment_data', str(payment_data))

        url = self.api_payments + '/payment'

        # call the api to process the payment
        self.r_payment = self.session.post(url, data=json.dumps(
            payment_data), headers=self.get_headers())

        payment_data = self.get_http_response_dict(self.session, self.r_payment)
        self.save_payment_data(SavedCardPaymentData, payment_data)

        self.validate_payment_data(payment_data, debug_tag=__name__)

        return payment_data

    @timeit
    def pay_with_credit_card(
        self, amount, type, number, exp_month, exp_year, cvv2, first_name, last_name
    ):
        formatted_amount = self.get_formatted_amount(amount)

        payment_data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [
                    {
                        "credit_card": {
                            "number": number,           # ie: "5500005555555559"
                            "type": type,             # ie: "mastercard"
                            "expire_month": exp_month,        # ie: 12
                            "expire_year": exp_year,         # ie: 2018
                            "cvv2": cvv2,             # ie: 111
                            "first_name": first_name,       # ie: "Betsy"
                            "last_name": last_name         # ie: "Buyer"
                        }
                    }
                ]
            },
            "transactions": [
                {
                    "amount": {
                        "total": formatted_amount,       # ie:"total": "7.47",
                        "currency": "USD"
                    },
                    "description": "This is the payment transaction description."
                }
            ]
        }

        # print('$$$$ payment_data:', str(payment_data))

        url = self.api_payments + '/payment'

        # call the api to process the payment
        self.r_payment = self.session.post(url, data=json.dumps(
            payment_data), headers=self.get_headers())

        # raise exceptions if the payment was not successful!
        self.validate_pay_with_credit_card(self.r_payment)

        payment_data = self.get_http_response_dict(self.session, self.r_payment)
        self.save_payment_data(CreditCardPaymentData, payment_data)

        self.validate_payment_data(payment_data, debug_tag=__name__)

        return payment_data

    def validate_payment_data(self, payment_data, debug_tag=''):

        # print('')
        # print('')
        # print('PAYMENT_DATA:', str(payment_data))
        # print('')
        # print('')

        # message = payment_data.get('message', '')
        name = payment_data.get('name')
        details = payment_data.get('details', [])

        if name is not None:
            if name == 'INVALID_RESOURCE_ID':
                raise self.InvalidSavedCardIdException()
        # print('payment_data:', str(payment_data))
        print('payment_data issues below:')
        for issue_data in details:
            err_msg = '%s - %s' % (name, str(issue_data.get('issue')))
            print(err_msg)
            raise self.PayPalException(err_msg)

    def validate_pay_with_credit_card(self, r):
        # TODO pass this while i work on testing
        pass  # TODO remove

        # message = r.get('message','')
        # name = r.get('name','')
        # details = r.get('details',{})
        # issue = details.get('issue','')
        # err_msg = 'message[%s] name[%s] issue[%s]' % (message, name, issue)
        # print(err_msg)

        # if self.r_payment.status_code >= 400:
        #     err_msg = 'HTTP [%s] %s' % (r.status_code, r.reason)
        #     raise self.PayWithCreditCardException(err_msg)

    def get_http_response_dict(self, session, r, verbose=False):
        # print( 'headers:', self.session.headers )
        # print( 'cookies:', str(self.session.cookies) )
        # status = r.status_code
        # if status <= 299:
        #     raise self.PayPalApiException()
        if verbose:
            print('HTTP [%s] %s' % (str(r.status_code), str(r.reason)))
            print('BODY [%s]' % str(r.text))
        if r.text is None or r.text == '':
            return {}
        # else its valid
        return json.loads(r.text)

    def validate_auth(self, r):
        # print('r.status_code:', r.status_code)
        if r.status_code >= 400:
            raise self.AuthException('PayPal.auth() error authenticating:' + str(r.reason))

    def auth(self):
        headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}
        post_data = {
            'grant_type': 'client_credentials'
        }
        # self.session = requests.Session()
        self.r_login = self.session.post(self.api_oauth_token,
                                         headers=headers, data=post_data,
                                         auth=(self.client_id, self.secret))
        self.validate_auth(self.r_login)

        # self.auth_data = json.loads( self.r_login.text )
        self.auth_data = self.get_http_response_dict(self.session, self.r_login)
        return self.auth_data

    def get_access_token(self):
        if self.auth_data is None:
            raise self.AuthException(
                'you must first call auth() before you can get an access_token')
        access_token = self.auth_data.get('access_token')
        if access_token is None:
            raise self.AuthException('unexpected error - access_token was None!')
        return access_token

    def save_card(self, card_data):
        """
        store a credit card using paypal's vault to make it easier to
        make payments using an associated token

        :param external_customer_id: also used for the "payer_id" field
        :param card_data:
        :param access_token:
        :return:
        """

        # make the call with the existing session object, performing a POST request
        url = self.api_vault + '/credit-cards'

        self.r_save_card = self.session.post(
            url, data=json.dumps(card_data), headers=self.get_headers())

        return self.get_http_response_dict(self.session, self.r_save_card)

    def delete_card(self, credit_card_id):
        """
        delete a stored credit card

        https://developer.paypal.com/docs/api/vault/#credit-card_delete
        """
        url = self.api_vault + '/credit-cards'
        url += '/%s' % credit_card_id

        self.r_delete_card = self.session.delete(url, headers=self.get_headers())
        return self.get_http_response_dict(self.session, self.r_delete_card)

    def show_card(self, credit_card_id):
        """
        show details for a stored card
        :param credit_card_id:
        :return:
        """
        url = self.api_vault + '/credit-cards'

        self.r_show_card_details = self.session.get(url, headers=self.get_headers())
        return self.get_http_response_dict(self.session, self.r_show_card_details)

    def list_cards(self, external_customer_id=None):
        """
        filter saved cards by their external customer id
        :param external_customer_id:
        :return:
        """

        get_params = ''
        if external_customer_id is not None:
            get_params += '?external_customer_id=%s' % external_customer_id

        url = self.api_vault + '/credit-cards'
        url += get_params

        self.r_list_cards = self.session.get(url, headers=self.get_headers())
        return self.get_http_response_dict(self.session, self.r_list_cards)

class Payout( object ):
    #
    #
    WITHDRAW_STATUS_PROCESSED = cash.withdraw.constants.WithdrawStatusConstants.Processed.value

    IN_PROGRESS_STATUSES = [
        'PROCESSING',
        'SUCCESS'
    ]

    PROCESSED_STATUSES = [
        'SUCCESS'  # notably not 'PROCESSED'
    ]

    api = settings.PAYPAL_REST_API_BASE
    client_id = settings.PAYPAL_CLIENT_ID
    secret = settings.PAYPAL_SECRET

    api_oauth_token = api + '/v1/oauth2/token'
    api_payout = api + '/v1/payments/payouts?sync_mode=true'

    def __init__(self, model_instance):
        self.STATUS_SUCCESS = cash.withdraw.models.WithdrawStatus.objects.get(pk=self.WITHDRAW_STATUS_PROCESSED)

        self.model_instance = model_instance

        self.session = None

        self.r_login = None
        self.r_payout = None

        self.sender_batch_id = None
        self.payout_batch_id = None

    def auth(self):
        headers = {
            'Accept' : 'application/json',
            'Accept-Language' : 'en_US'
        }
        post_data = {
            'grant_type' : 'client_credentials'
        }
        self.session = requests.Session()
        self.r_login = self.session.post( self.api_oauth_token,
                                          headers=headers, data=post_data,
                                          auth=(self.client_id, self.secret))
        print( self.r_login.status_code )
        print( self.api_oauth_token )
        print( self.r_login.text )

        self.model_instance.auth_status = str(self.r_login.status_code)
        self.model_instance.save()
        return json.loads( self.r_login.text )

    def payout_async(self, withdraws=[]):
        """
        call the payout() method using a celery task to perform asynchronous payout

        :param withdraws:
        :return:
        """
        pass

    def payout(self, get_until_processed=True):
        """
        this method takes very tangible time - usually like 15-30 seconds.

        if 'get_until_processed' is set to False, this will return immediately,
        once the payout has been submitted, but paypal will still take some time
        to full process the payout so you will likely not know at this point
        if the payout has succeeded or failed. use get() to check on the status

        :param to_email:
        :param amount:
        :return:
        """

        #
        # login
        if self.session is None:
            auth_response = self.auth()

        if self.model_instance.paypal_transaction:
            # if it exists, we need to check it we ever paid this transaction out !
            check_get_json = self.get( batch_id=self.model_instance.paypal_transaction, save=False )
            batch_status = check_get_json.get('batch_header').get('batch_status')
            if batch_status in self.IN_PROGRESS_STATUSES:
                tid = self.model_instance.paypal_transaction
                msg = 'transaction has already been processed! paypal_transaction: ' + str(tid)
                print( msg )
                #raise Exception( msg )
                return

        #
        # issue the payout
        j = json.loads( self.r_login.text )
        headers = {
            'Content-Type'  : 'application/json',
            'Authorization' : '%s %s' % (j.get('token_type'), j.get('access_token'))
        }
        self.sender_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        post_data = {
            "sender_batch_header" : {
                "sender_batch_id"   : "%s" % self.sender_batch_id,
                "email_subject"     : "You have a Payout!",
                "recipient_type"    : "EMAIL"
            },
            "items" : [
                {
                    "recipient_type" : "EMAIL",
                    "amount" : {
                        "value"     : "%s" % str( float( abs( self.model_instance.amount ) ) ),
                        "currency"  : "USD"
                    },
                    "note"              : "Thanks for your patronage!",
                    "sender_item_id"    : "201403140001",
                    "receiver"          : "%s" % self.model_instance.email
                }
            ]
        }
        #j = json.loads( json.dumps( post_data ) )
        self.r_payout = self.session.post( self.api_payout,
                                           headers=headers,
                                           data=json.dumps( post_data ) )
        print( self.r_payout.status_code )
        print( 'POST', self.api_payout )
        print( self.r_payout.text )
        j = json.loads( self.r_payout.text )

        #
        # this error is possible:
        # {"name":"VALIDATION_ERROR","message":"Invalid request - see details.",
        #   "debug_id":"943be7f1a0f95",
        #   "information_link":"https://developer.paypal.com/webapps/developer/docs/api/#VALIDATION_ERROR",
        #   "details":[{"field":"items[0].receiver","issue":"Required field missing"}]}
        try:
            self.payout_batch_id = j.get('batch_header').get('payout_batch_id')
        except AttributeError: # ie: 'batch_header' didnt exist
            # stash error in paypal model withdraw
            self.model_instance.paypal_errors = self.r_payout.text
            self.model_instance.save()
            print( self.r_payout.text )
            print( 'payout failed! check the admin page for withdraws for error messages from paypal')
            return

        #
        # set the payal transaction id in the model, along with the current status
        self.paypal_transaction = self.payout_batch_id
        self.model_instance.paypal_transaction = self.paypal_transaction
        self.model_instance.payout_status = j.get('batch_header').get('batch_status')
        self.model_instance.save()

        if get_until_processed:
            #
            # call get() until we've updated to the PROCESSED status
            while True: # scary - but we will make sure to add very long timeout to the calling task
                time.sleep( 5.0 )
                get_json = self.get()
                payout_status = get_json.get('batch_header').get('batch_status')
                print( 'payout GET status:', payout_status )
                if payout_status in self.PROCESSED_STATUSES: # ie: failure may be in here!
                    #
                    # update the master success in the admin, plus any papal error
                    self.model_instance.status = self.STATUS_SUCCESS
                    self.model_instance.save()
                    break

        return j

    def get(self, batch_id=None, save=True):
        if batch_id is None:
            batch_id = self.payout_batch_id
        print( 'get', batch_id )

        j = json.loads( self.r_login.text )
        headers = {
            'Authorization' : '%s %s' % (j.get('token_type'), j.get('access_token'))
        }
        self.r_get = self.session.get( self.api_payout + '/' + str(batch_id), headers=headers )
        print( self.r_get.status_code )
        print( 'GET', self.api_payout )
        print( self.r_get.text )

        j = json.loads( self.r_get.text )

        if save:
            self.model_instance.get_status = j.get('batch_header').get('batch_status')
            self.model_instance.save()

        return j

    def payout_debug_test_error_50_percent(self):
        """
        delays for a few seconds, and then, randomly decides to succeed or error.

        returns a randomly generated string of 12 characters upon success

        :return:
        """
        r = random.Random()
        status = bool( r.randrange(0, 2) )     # randomly a 0 or a 1

        random_transaction_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        self.debug_delay_sec_payout( status=status )

# def test_app():
#     heartbeat.delay()
#
# def test_payout(pk=1):
#     #p = Payout( to_email='testtest@coderden.com', amount=0.10 )
#     #return payout.delay( instance=p )
#     ppw = cash.withdraw.models.PayPalWithdraw.objects.get( pk = pk )
#     p = Payout( model_instance=ppw )
#     return payout.apply_async( (p, ), serializer='pickle' )