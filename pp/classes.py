
from mysite import settings
import requests
import random
import string
import json
import time

class Payout( object ):

    api = 'https://api.sandbox.paypal.com' # 'https://api.paypal.com'

    api_oauth_token = api + '/v1/oauth2/token'
    api_payout      = api + '/v1/payments/payouts'

    def __init__(self):
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
        return json.loads( self.r_login.text )

    def payout(self, to_email='testtest@coderden.com', amount=0.10):
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
                        "value"     : "%s" % str(amount),
                        "currency"  : "USD"
                    },
                    "note"              : "Thanks for your patronage!",
                    "sender_item_id"    : "201403140001",
                    "receiver"          : "%s" % to_email
                }
            ]
        }
        #j = json.loads( json.dumps( post_data ) )
        self.r_payout = self.session.post( self.api_payout,
                                           headers=headers,
                                           data=json.dumps( post_data ) )
        print( self.r_payout.status_code )
        print( self.r_payout.text )
        j = json.loads( self.r_payout.text )
        self.payout_batch_id = j.get('batch_header').get('payout_batch_id')
        return j

    def get(self, batch_id=None):
        if batch_id is None:
            batch_id = self.payout_batch_id
        print( 'get', batch_id )

        j = json.loads( self.r_login.text )
        headers = {
            'Authorization' : '%s %s' % (j.get('token_type'), j.get('access_token'))
        }
        self.r_get = self.session.get( self.api_payout + '/' + str(batch_id), headers=headers )
        print( self.r_get.status_code )
        return json.loads( self.r_get.text )

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
