
from mysite import settings
import requests
import random
import string
import json
import time

# import mysite.exceptions
from mysite.celery_app import heartbeat, payout

import cash.withdraw.constants
import cash.withdraw.models

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

    api = 'https://api.sandbox.paypal.com' # 'https://api.paypal.com'

    api_oauth_token = api + '/v1/oauth2/token'
    api_payout      = api + '/v1/payments/payouts'

    def __init__(self, model_instance):
        self.STATUS_SUCCESS = cash.withdraw.models.WithdrawStatus.objects.get(pk=self.WITHDRAW_STATUS_PROCESSED)

        self.model_instance = model_instance

        self.client_id  = 'ATqLK_YEFwhEGOF_28TQLxXq-MG88suXKQZm0k4UjrfkrvXwxSRbv6mgPO8moTdLHeJ3zFb-t8sBdKLg'
        self.secret     = 'EFuyMSsA8EcOabrJBqPvbUW-0ZnRJ8ym8XrxPDje9GeTuJOF-Dxcn4gLI9hNR79chUE_MO4Y_u6mMQrQ'

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

        # response to payout_batch_id (the master of all of the items)
        # {'batch_header': {'fees': {'value': '0.0', 'currency': 'USD'}, 'amount': {'value': '0.01', 'currency': 'USD'}, 'time_completed': '2015-04-22T04:17:34Z', 'time_created': '2015-04-22T04:17:09Z', 'payout_batch_id': 'AP393JT3TEUF2', 'batch_status': 'SUCCESS', 'sender_batch_header': {'sender_batch_id': 'FUFFEPGMVBGX', 'email_subject': 'You have a Payout!'}}, 'items': [{'links': [{'method': 'GET', 'href': 'https://api.sandbox.paypal.com/v1/payments/payouts-item/HVBG5X7F9MYSS', 'rel': 'item'}], 'payout_item': {'recipient_type': 'EMAIL', 'receiver': 'testtest@coderden.com', 'sender_item_id': '201403140001', 'note': 'Thanks for your patronage!', 'amount': {'value': '0.01', 'currency': 'USD'}}, 'transaction_id': '68696867XP9554523', 'transaction_status': 'SUCCESS', 'payout_item_fee': {'value': '0.0', 'currency': 'USD'}, 'time_processed': '2015-04-22T04:17:26Z', 'payout_batch_id': 'AP393JT3TEUF2', 'payout_item_id': 'HVBG5X7F9MYSS'}], 'links': [{'method': 'GET', 'href': 'https://api.sandbox.paypal.com/v1/payments/payouts/AP393JT3TEUF2', 'rel': 'self'}]}

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

    def debug_delay_sec_payout(self, t=5.0, status=False):
        time.sleep( t )

        if status == False:
            raise Exception('debug_delay_sec_payout - randomized exception')

        print( 'the task [debug_delay_sec_payout] had this for status:', str(status) )

def test_app():
    heartbeat.delay()

def test_payout(pk=1):
    #p = Payout( to_email='testtest@coderden.com', amount=0.10 )
    #return payout.delay( instance=p )
    ppw = cash.withdraw.models.PayPalWithdraw.objects.get( pk = pk )
    p = Payout( model_instance=ppw )
    return payout.apply_async( (p, ), serializer='pickle' )