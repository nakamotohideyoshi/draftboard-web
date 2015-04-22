
from mysite import settings
import requests
import random
import string
import json

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
        random_batch_id = ''.join(random.choice(string.ascii_uppercase) for i in range(12))
        post_data = {
            "sender_batch_header" : {
                "sender_batch_id"   : "%s" % random_batch_id,
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
        return json.loads( self.r_payout.text )

