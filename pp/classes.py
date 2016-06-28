#
# classes.py

from mysite import settings
import requests
import random
import json
from util.timesince import timeit
import paypalrestsdk as paypal
# import logging
# logging.basicConfig(level=logging.INFO)

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
    check_digit = luhn_checksum(int(partial_card_number) * 10)   # Append a zero check digit to the partial number and calculate checksum
    return check_digit if check_digit == 0 else 10 - check_digit # If the (sum mod 10) == 0, then the check digit is 0
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

    class InvalidCardFieldException(Exception): pass

    class InvalidBillingFieldException(Exception): pass

    BILLING_ADDRESS_DATA    = 'billing_address'

    # will get set when external_customer_id set
    PAYER_ID                = 'payer_id'

    EXTERNAL_CUSTOMER_ID    = 'external_customer_id'        # string
    TYPE                    = 'type'                        # card type, ie: 'visa'
    NUMBER                  = 'number'                      # credit card number, ie: "4417119669820331" (string)
    EXPIRE_MONTH            = 'expire_month'                # exp month (string)
    EXPIRE_YEAR             = 'expire_year'                 # exp year (string)
    CVV2                    = 'cvv2'                        # cvv2 code
    FIRST_NAME              = 'first_name'
    LAST_NAME               = 'last_name'

    # used for validation
    CARD_FIELDS = [
        EXTERNAL_CUSTOMER_ID, TYPE, NUMBER, EXPIRE_MONTH, EXPIRE_YEAR, FIRST_NAME, LAST_NAME, CVV2
    ]

    # billing address information
    LINE_1                  = 'line1'                       # first line of address
    CITY                    = 'city'                        # ie: 'Saratoga' (string)
    COUNTRY_CODE            = 'country_code'                # ie: 'US'
    STATE                   = 'state'                       # ie: 'CA'
    POSTAL_CODE             = 'postal_code'                 # ie: '95070' (string)

    # used for validation
    BILLING_FIELDS = [
        LINE_1, CITY, COUNTRY_CODE, STATE, POSTAL_CODE
    ]

    def __init__(self, data=None):
        self.data = data
        if self.data is None:
            self.data = {
                self.PAYER_ID : None,
                self.EXTERNAL_CUSTOMER_ID : None,
                self.TYPE : None,
                self.NUMBER : None,
                self.EXPIRE_MONTH : None,
                self.EXPIRE_YEAR : None,
                self.CVV2 : None,
                self.FIRST_NAME : None,
                self.LAST_NAME : None,
                self.BILLING_ADDRESS_DATA : {
                    self.LINE_1 : None,
                    self.CITY : None,
                    self.COUNTRY_CODE : None,
                    self.STATE : None,
                    self.POSTAL_CODE : None,
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

class SavedCard(object):

    def __init__(self, data):
        self.data = data

    # TODO extract fields of the save card and do whatever to store it

class PayPal(object):
    #
    # apparently this is possible:
    # HTTP [503] Service Unavailable
    # BODY [{"name":"INTERNAL_SERVICE_ERROR","information_link":"https://api.sandbox.paypal.com/docs/api/#INTERNAL_SERVICE_ERROR","debug_id":"1635acf4b1f6c"}]

    # this can also happen during payments:
    # In [9]: r = p.pay_with_credit_card(25, 'mastercard', '5500005555555559', 12, 2018, 111, 'Betsy', 'Buyer')
    # headers: {'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'python-requests/2.6.0 CPython/3.4.3 Linux/3.13.0-49-generic', 'Accept': '*/*', 'Connection': 'keep-alive'}
    # cookies: <RequestsCookieJar[<Cookie X-PP-SILOVER=name%3DSANDBOX3.API.1%26silo_version%3D1880%26app%3Dplatformapiserv%26TIME%3D3092539479%26HTTP_X_PP_AZ_LOCATOR%3D for .paypal.com/>]>
    # HTTP [400] Bad Request
    # BODY [{"name":"UNKNOWN_ERROR","message":"An unknown error has occurred","information_link":"https://developer.paypal.com/webapps/developer/docs/api/#UNKNOWN_ERROR","debug_id":"ce216adf53370"}]

    class UnimplementedMethodException(Exception): pass

    class AuthException(Exception): pass

    class PayWithCreditCardException(Exception): pass

    class PayWithSavedCardException(Exception): pass

    class InvalidSavedCardIdException(Exception): pass

    # TODO add pay wtih paypal account exception

    api = 'https://api.sandbox.paypal.com' # 'https://api.paypal.com'

    api_vault       = api + '/v1/vault'
    api_payments    = api + '/v1/payments'
    api_oauth_token = api + '/v1/oauth2/token'

    def __init__(self):
        self.client_id  = 'ARqP3lkXhhR_jmm6NkyoKQfuOcBsn1KBYtlzZGHEvGDCQ-ajNoxpQD2mDScpT6tkgsI7qFgVJ-KgzpFE'
        self.secret     = 'EOKSd-HCNfWE17mu8e7uyjs2egSla2yXs7joweXCLdimCY8yv-FcCx7LeP1do0gMb9vExJSmjyw9hwRu'
        self.session    = requests.Session()
        self.auth_data  = None # set when auth() has been called

        # response values for debugging - officially speaking, dont use outside of the methods that set them
        self.r_login                = None
        self.r_save_card            = None
        self.r_delete_card          = None
        self.r_show_card_details    = None
        self.r_payment              = None

    def get_headers(self):
        headers = { 'Content-Type' : 'application/json',
                    'Authorization' : 'Bearer %s' % self.get_access_token() }
        return headers

    def pay_with_paypal(self):
        """
        https://developer.paypal.com/docs/integration/web/accept-paypal-payment/
        """
        # TODO - this requires a bit more complicated flow between us and paypal
        raise self.UnimplementedMethodException('pay_with_paypal() - TODO')

    # def test_tls(self):
    #     paypal.configure({
    #       "mode": "security-test-sandbox", # sandbox or live
    #       "client_id": self.client_id,
    #       "client_secret": self.secret })
    #
    #     # Payment
    #     # A Payment Resource; create one using
    #     # the above types and intent as 'sale'
    #     payment = paypal.Payment({
    #         "intent": "sale",
    #
    #         # Payer
    #         # A resource representing a Payer that funds a payment
    #         # Payment Method as 'paypal'
    #         "payer": {
    #             "payment_method": "paypal"},
    #
    #         # Redirect URLs
    #         "redirect_urls": {
    #             "return_url": "http://localhost:3000/payment/execute",
    #             "cancel_url": "http://localhost:3000/"},
    #
    #         # Transaction
    #         # A transaction defines the contract of a
    #         # payment - what is the payment for and who
    #         # is fulfilling it.
    #         "transactions": [{
    #
    #             # ItemList
    #             "item_list": {
    #                 "items": [{
    #                     "name": "item",
    #                     "sku": "item",
    #                     "price": "5.00",
    #                     "currency": "USD",
    #                     "quantity": 1}]},
    #
    #             # Amount
    #             # Let's you specify a payment amount.
    #             "amount": {
    #                 "total": "5.00",
    #                 "currency": "USD"},
    #             "description": "This is the payment transaction description."}]})
    #
    #     # Create Payment and return status
    #     if payment.create():
    #         print("Payment[%s] created successfully" % (payment.id))
    #         # Redirect the user to given approval url
    #         for link in payment.links:
    #             if link.method == "REDIRECT":
    #                 # Convert to str to avoid google appengine unicode issue
    #                 # https://github.com/paypal/rest-api-sdk-python/pull/58
    #                 redirect_url = str(link.href)
    #                 print("Redirect for approval: %s" % (redirect_url))
    #     else:
    #         print("Error while creating payment:")
    #         print(payment.error)

    def get_formatted_amount(self, amount):
        """
        This method expects a float amount [sort of].

        However, if the amount is an integer or a string
        we attempt to format it into a float for ease of use.

        :param amount:
        :return:
        """
        formatted_amount = amount
        if isinstance(formatted_amount, str) or isinstance(formatted_amount, int):
            # attempt to cast to float() and format into 2 decimal place string
            formatted_amount = '%.2f' % float(formatted_amount)
        return formatted_amount

    def pay_with_saved_card(self, amount, external_customer_id, saved_card_id):
        formatted_amount = self.get_formatted_amount(amount)

        payment_data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [
                    {
                        "credit_card_token": {
                            "credit_card_id" : saved_card_id,              # ie: "CARD-1MD19612EW4364010KGFNJQI",
                            "payer_id" : external_customer_id               # ie: "ppuser12345",
                        }
                    }
                ]
            },
            "transactions": [
                {
                    "amount": {
                        "total" : formatted_amount,       # ie:"total": "7.47",
                        "currency": "USD"
                    },
                    "description": "This is the payment transaction description."
                }
            ]
        }

        #print('payment_data', str(payment_data))

        url = self.api_payments + '/payment'

        # call the api to process the payment
        self.r_payment = self.session.post(url, data=json.dumps(payment_data), headers=self.get_headers())

        payment_data = self.get_http_response_dict(self.session, self.r_payment)

        self.validate_payment_data(payment_data, debug_tag=__name__)

        return payment_data

    @timeit
    def pay_with_credit_card(self, amount, type, number, exp_month, exp_year, cvv2, first_name, last_name):
        formatted_amount = self.get_formatted_amount(amount)

        payment_data = {
            "intent": "sale",
            "payer": {
                "payment_method": "credit_card",
                "funding_instruments": [
                    {
                        "credit_card": {
                            "number"        : number,           # ie: "5500005555555559"
                            "type"          : type,             # ie: "mastercard"
                            "expire_month"  : exp_month,        # ie: 12
                            "expire_year"   : exp_year,         # ie: 2018
                            "cvv2"          : cvv2,             # ie: 111
                            "first_name"    : first_name,       # ie: "Betsy"
                            "last_name"     : last_name         # ie: "Buyer"
                        }
                    }
                ]
            },
            "transactions": [
                {
                    "amount": {
                        "total" : formatted_amount,       # ie:"total": "7.47",
                        "currency": "USD"
                    },
                    "description": "This is the payment transaction description."
                }
            ]
        }

        #print('$$$$ payment_data:', str(payment_data))

        url = self.api_payments + '/payment'

        # call the api to process the payment
        self.r_payment = self.session.post(url, data=json.dumps(payment_data), headers=self.get_headers())

        # raise exceptions if the payment was not successful!
        self.validate_pay_with_credit_card(self.r_payment)

        payment_data = self.get_http_response_dict(self.session, self.r_payment)

        self.validate_payment_data(payment_data, debug_tag=__name__)

        return payment_data

    def validate_payment_data(self, payment_data, debug_tag=''):

        # print('')
        # print('')
        # print('PAYMENT_DATA:', str(payment_data))
        # print('')
        # print('')

        message = payment_data.get('message','')
        name = payment_data.get('name')
        details = payment_data.get('details',{})

        if name is not None:
            if name == 'INVALID_RESOURCE_ID':
                raise self.InvalidSavedCardIdException()

        for issue_data in details:
            err_msg = '        message[%s] name[%s] issue[%s]' % (message, name, str(issue_data.get('issue')))
            print(err_msg)

    def validate_pay_with_credit_card(self, r):
        # TODO pass this while i work on testing
        pass # TODO remove

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
        #print( 'headers:', self.session.headers )
        #print( 'cookies:', str(self.session.cookies) )
        #status = r.status_code
        # if status <= 299:
        #     raise self.PayPalApiException()
        if verbose:
            print( 'HTTP [%s] %s' % (str(r.status_code), str(r.reason)) )
            print( 'BODY [%s]' % str(r.text) )
        if r.text is None or r.text == '':
            return {}
        # else its valid
        return json.loads(r.text)

    def validate_auth(self, r):
        #print('r.status_code:', r.status_code)
        if r.status_code >= 400:
            raise self.AuthException('PayPal.auth() error authenticating:' + str(r.reason))

    def auth(self):
        headers = { 'Accept' : 'application/json', 'Accept-Language' : 'en_US' }
        post_data = {
            'grant_type' : 'client_credentials'
        }
        #self.session = requests.Session()
        self.r_login = self.session.post( self.api_oauth_token,
                                          headers=headers, data=post_data,
                                          auth=(self.client_id, self.secret))
        self.validate_auth(self.r_login)

        #self.auth_data = json.loads( self.r_login.text )
        self.auth_data = self.get_http_response_dict(self.session, self.r_login)
        return self.auth_data

    def get_access_token(self):
        if self.auth_data is None:
            raise self.AuthException('you must first call auth() before you can get an access_token')
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

        self.r_save_card = self.session.post(url, data=json.dumps(card_data), headers=self.get_headers())

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

# #
# ##########################################################################################
# # old code
# ##########################################################################################
# class Payout( object ):
#     #
#     #
#     WITHDRAW_STATUS_PROCESSED = cash.withdraw.constants.WithdrawStatusConstants.Processed.value
#
#     IN_PROGRESS_STATUSES = [
#         'PROCESSING',
#         'SUCCESS'
#     ]
#
#     PROCESSED_STATUSES = [
#         'SUCCESS'  # notably not 'PROCESSED'
#     ]
#
#     api = 'https://api.sandbox.paypal.com' # 'https://api.paypal.com'
#
#     api_oauth_token = api + '/v1/oauth2/token'
#     api_payout      = api + '/v1/payments/payouts'
#
#     def __init__(self, model_instance):
#         self.STATUS_SUCCESS = cash.withdraw.models.WithdrawStatus.objects.get(pk=self.WITHDRAW_STATUS_PROCESSED)
#
#         self.model_instance = model_instance
#
#         self.client_id  = 'ATqLK_YEFwhEGOF_28TQLxXq-MG88suXKQZm0k4UjrfkrvXwxSRbv6mgPO8moTdLHeJ3zFb-t8sBdKLg'
#         self.secret     = 'EFuyMSsA8EcOabrJBqPvbUW-0ZnRJ8ym8XrxPDje9GeTuJOF-Dxcn4gLI9hNR79chUE_MO4Y_u6mMQrQ'
#
#         self.session = None
#
#         self.r_login = None
#         self.r_payout = None
#
#         self.sender_batch_id = None
#         self.payout_batch_id = None
#
#     def auth(self):
#         headers = {
#             'Accept' : 'application/json',
#             'Accept-Language' : 'en_US'
#         }
#         post_data = {
#             'grant_type' : 'client_credentials'
#         }
#         self.session = requests.Session()
#         self.r_login = self.session.post( self.api_oauth_token,
#                                           headers=headers, data=post_data,
#                                           auth=(self.client_id, self.secret))
#         print( self.r_login.status_code )
#         print( self.api_oauth_token )
#         print( self.r_login.text )
#
#         self.model_instance.auth_status = str(self.r_login.status_code)
#         self.model_instance.save()
#         return json.loads( self.r_login.text )
#
#     def payout_async(self, withdraws=[]):
#         """
#         call the payout() method using a celery task to perform asynchronous payout
#
#         :param withdraws:
#         :return:
#         """
#         pass
#
#     def payout(self, get_until_processed=True):
#         """
#         this method takes very tangible time - usually like 15-30 seconds.
#
#         if 'get_until_processed' is set to False, this will return immediately,
#         once the payout has been submitted, but paypal will still take some time
#         to full process the payout so you will likely not know at this point
#         if the payout has succeeded or failed. use get() to check on the status
#
#         :param to_email:
#         :param amount:
#         :return:
#         """
#
#         #
#         # login
#         if self.session is None:
#             auth_response = self.auth()
#
#         if self.model_instance.paypal_transaction:
#             # if it exists, we need to check it we ever paid this transaction out !
#             check_get_json = self.get( batch_id=self.model_instance.paypal_transaction, save=False )
#             batch_status = check_get_json.get('batch_header').get('batch_status')
#             if batch_status in self.IN_PROGRESS_STATUSES:
#                 tid = self.model_instance.paypal_transaction
#                 msg = 'transaction has already been processed! paypal_transaction: ' + str(tid)
#                 print( msg )
#                 #raise Exception( msg )
#                 return
#
#         #
#         # issue the payout
#         j = json.loads( self.r_login.text )
#         headers = {
#             'Content-Type'  : 'application/json',
#             'Authorization' : '%s %s' % (j.get('token_type'), j.get('access_token'))
#         }
#         self.sender_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
#         post_data = {
#             "sender_batch_header" : {
#                 "sender_batch_id"   : "%s" % self.sender_batch_id,
#                 "email_subject"     : "You have a Payout!",
#                 "recipient_type"    : "EMAIL"
#             },
#             "items" : [
#                 {
#                     "recipient_type" : "EMAIL",
#                     "amount" : {
#                         "value"     : "%s" % str( float( abs( self.model_instance.amount ) ) ),
#                         "currency"  : "USD"
#                     },
#                     "note"              : "Thanks for your patronage!",
#                     "sender_item_id"    : "201403140001",
#                     "receiver"          : "%s" % self.model_instance.email
#                 }
#             ]
#         }
#         #j = json.loads( json.dumps( post_data ) )
#         self.r_payout = self.session.post( self.api_payout,
#                                            headers=headers,
#                                            data=json.dumps( post_data ) )
#         print( self.r_payout.status_code )
#         print( 'POST', self.api_payout )
#         print( self.r_payout.text )
#         j = json.loads( self.r_payout.text )
#
#         #
#         # this error is possible:
#         # {"name":"VALIDATION_ERROR","message":"Invalid request - see details.",
#         #   "debug_id":"943be7f1a0f95",
#         #   "information_link":"https://developer.paypal.com/webapps/developer/docs/api/#VALIDATION_ERROR",
#         #   "details":[{"field":"items[0].receiver","issue":"Required field missing"}]}
#         try:
#             self.payout_batch_id = j.get('batch_header').get('payout_batch_id')
#         except AttributeError: # ie: 'batch_header' didnt exist
#             # stash error in paypal model withdraw
#             self.model_instance.paypal_errors = self.r_payout.text
#             self.model_instance.save()
#             print( self.r_payout.text )
#             print( 'payout failed! check the admin page for withdraws for error messages from paypal')
#             return
#
#         #
#         # set the payal transaction id in the model, along with the current status
#         self.paypal_transaction = self.payout_batch_id
#         self.model_instance.paypal_transaction = self.paypal_transaction
#         self.model_instance.payout_status = j.get('batch_header').get('batch_status')
#         self.model_instance.save()
#
#         if get_until_processed:
#             #
#             # call get() until we've updated to the PROCESSED status
#             while True: # scary - but we will make sure to add very long timeout to the calling task
#                 time.sleep( 5.0 )
#                 get_json = self.get()
#                 payout_status = get_json.get('batch_header').get('batch_status')
#                 print( 'payout GET status:', payout_status )
#                 if payout_status in self.PROCESSED_STATUSES: # ie: failure may be in here!
#                     #
#                     # update the master success in the admin, plus any papal error
#                     self.model_instance.status = self.STATUS_SUCCESS
#                     self.model_instance.save()
#                     break
#
#         return j
#
#     def get(self, batch_id=None, save=True):
#         if batch_id is None:
#             batch_id = self.payout_batch_id
#         print( 'get', batch_id )
#
#         j = json.loads( self.r_login.text )
#         headers = {
#             'Authorization' : '%s %s' % (j.get('token_type'), j.get('access_token'))
#         }
#         self.r_get = self.session.get( self.api_payout + '/' + str(batch_id), headers=headers )
#         print( self.r_get.status_code )
#         print( 'GET', self.api_payout )
#         print( self.r_get.text )
#
#         j = json.loads( self.r_get.text )
#
#         if save:
#             self.model_instance.get_status = j.get('batch_header').get('batch_status')
#             self.model_instance.save()
#
#         return j
#
#         # response to payout_batch_id (the master of all of the items)
#         # {'batch_header': {'fees': {'value': '0.0', 'currency': 'USD'}, 'amount': {'value': '0.01', 'currency': 'USD'}, 'time_completed': '2015-04-22T04:17:34Z', 'time_created': '2015-04-22T04:17:09Z', 'payout_batch_id': 'AP393JT3TEUF2', 'batch_status': 'SUCCESS', 'sender_batch_header': {'sender_batch_id': 'FUFFEPGMVBGX', 'email_subject': 'You have a Payout!'}}, 'items': [{'links': [{'method': 'GET', 'href': 'https://api.sandbox.paypal.com/v1/payments/payouts-item/HVBG5X7F9MYSS', 'rel': 'item'}], 'payout_item': {'recipient_type': 'EMAIL', 'receiver': 'testtest@coderden.com', 'sender_item_id': '201403140001', 'note': 'Thanks for your patronage!', 'amount': {'value': '0.01', 'currency': 'USD'}}, 'transaction_id': '68696867XP9554523', 'transaction_status': 'SUCCESS', 'payout_item_fee': {'value': '0.0', 'currency': 'USD'}, 'time_processed': '2015-04-22T04:17:26Z', 'payout_batch_id': 'AP393JT3TEUF2', 'payout_item_id': 'HVBG5X7F9MYSS'}], 'links': [{'method': 'GET', 'href': 'https://api.sandbox.paypal.com/v1/payments/payouts/AP393JT3TEUF2', 'rel': 'self'}]}
#
#     def payout_debug_test_error_50_percent(self):
#         """
#         delays for a few seconds, and then, randomly decides to succeed or error.
#
#         returns a randomly generated string of 12 characters upon success
#
#         :return:
#         """
#         r = random.Random()
#         status = bool( r.randrange(0, 2) )     # randomly a 0 or a 1
#
#         random_transaction_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
#         self.debug_delay_sec_payout( status=status )
#
#     def debug_delay_sec_payout(self, t=5.0, status=False):
#         time.sleep( t )
#
#         if status == False:
#             raise Exception('debug_delay_sec_payout - randomized exception')
#
#         print( 'the task [debug_delay_sec_payout] had this for status:', str(status) )
#
# def test_app():
#     heartbeat.delay()
#
# def test_payout(pk=1):
#     #p = Payout( to_email='testtest@coderden.com', amount=0.10 )
#     #return payout.delay( instance=p )
#     ppw = cash.withdraw.models.PayPalWithdraw.objects.get( pk = pk )
#     p = Payout( model_instance=ppw )
#     return payout.apply_async( (p, ), serializer='pickle' )