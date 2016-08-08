#
# tests.py

from test.classes import AbstractTest
from pp.classes import (
    PayPal,
    CardData,

    VZero,
    VZeroShipping,
    VZeroTransaction,
)
from pp.serializers import (
    VZeroShippingSerializer,
    VZeroDepositSerializer,
)
from util.timesince import timeit

# to achieve faster testing you can run these tests with
#    $> ./manage.py test pp --keepdb
# because these tests do no rely on any migrations
# although django sets them up the first time anyways

CARD_DATA_1_USER = "carddata1"
CARD_DATA_1 = {
    "payer_id":CARD_DATA_1_USER,
    "external_customer_id":CARD_DATA_1_USER,
    "type":"visa",
    "number":"4417119669820331",
    "expire_month":"11",
    "expire_year":"2018",
    "cvv2" : "111",
    "first_name":"Betsy",
    "last_name":"Buyer",
    "billing_address":{
        "line1":"111 First Street",
        "city":"Saratoga",
        "country_code":"US",
        "state":"CA",
        "postal_code":"95070"
    }
}
CARD_DATA_FOR_DELETE_1_USER = 'userdelete1'
CARD_DATA_FOR_DELETE_1 = CARD_DATA_1.copy()
CARD_DATA_FOR_DELETE_1['payer_id'] = CARD_DATA_FOR_DELETE_1_USER
CARD_DATA_FOR_DELETE_1['external_customer_id'] = CARD_DATA_FOR_DELETE_1_USER

class TestCardData(AbstractTest):

    def setUp(self):
        pass # TODO ?

    def test_set_card_field(self):
        pass # TODO

    def test_set_billing_field(self):
        pass # TODO

    def test_card_data_from_dict(self):
        cd = CardData(CARD_DATA_1)

class TestPayPal(AbstractTest):

    def setUp(self):
        pass # TODO ?

    @timeit
    def test_auth(self):
        pp = PayPal()
        pp.client_id = 'invalid-client-id'
        pp.secret = 'invalid-secret'
        self.assertRaises(
            PayPal.AuthException,
            lambda: pp.auth(),
        )

    def test_list_cards(self):
        pp = PayPal()
        pp.auth()
        cards = pp.list_cards()

    def test_save_card_before_auth_called(self):
        pp = PayPal()

        self.assertRaises(
            PayPal.AuthException,
            lambda: pp.save_card(CARD_DATA_1),
        )

    def test_save_card(self):
        pp = PayPal()
        pp.auth()
        card = pp.save_card(CARD_DATA_1)
        #print('new saved card:', str(card))

    def test_delete_card(self):
        """
        paypal claims the "delete card" method simply deletes details of the card,
        so im not sure if it will show up in the list after being deleted

        :return:
        """
        pp = PayPal()
        pp.auth()
        card = pp.save_card(CARD_DATA_FOR_DELETE_1)

        # now delete it
        card_id_for_delete = card.get('id')
        #print('card_id_for_delete:', str(card_id_for_delete))
        delete_card_response = pp.delete_card(card_id_for_delete)
        #print('delete_card_response:', str(delete_card_response))

        # get the list of credit cards to see if its still in there
        list_cards = pp.list_cards()
        #print('list_cards after delete_card() called:', str(list_cards))
        for list_card in list_cards.get('items'):
            if card_id_for_delete == list_card.get('id'):
                err_msg = 'card [%s] not deleted? it still shows up in list_cards() data' % card_id_for_delete
                raise Exception(err_msg)

    def test_pay_with_credit_card_exception(self):
        """
        test using a bad cc number or other things that will raise exceptions
        when trying to pay with a regular credit card.
        """
        pass # TODO

    def test_pay_with_credit_card(self):
        """
        NOTE: its mandatory that you are using sandbox credit card information
        found on an account in https://developer.paypal.com/developer/accounts/ !

        test making a payment with a credit card, in particular this is NOT a saved credit card payment.
        :return:
        """
        pp = PayPal()
        pp.auth()

        card_data = CardData(CARD_DATA_1)

        # {"type":"visa","number":"4032036765082399","exp_month":"12","exp_year":"2020","cvv2":"012"}
        #type = card_data.get_type()
        type = 'visa'
        #number = card_data.get_number() # originally this was not a valid credit card complying with "mod-10"
        #number = '4111111111111111' # test
        #number = '4012888888881881' # test
        #number = '4222222222222' # test
        number = '4032036765082399' #
        #exp_month = card_data.get_exp_month()
        exp_month = '06'
        #exp_year = card_data.get_exp_year()
        exp_year = '2021'
        #cvv2 = card_data.get_cvv2()
        cvv2 = '000'
        first_name = card_data.get_first_name()
        last_name = card_data.get_last_name()

        amount = 20.01
        # pay_with_credit_card(self, amount, type, number, exp_month, exp_year, cvv2, first_name, last_name)
        payment_data = pp.pay_with_credit_card(amount, type, number, exp_month, exp_year,
                                                                cvv2, first_name, last_name)

        # print('>>> payment_data:', str(payment_data))

    def test_pay_with_saved_card_raises_invalid_saved_card_id_exception(self):
        pp = PayPal()
        pp.auth()

        # use a dummy card id we know cant exist
        amount = 21.88
        external_customer_id = 'somecustomer_username'
        saved_card_id = 'invalid_saved_card_id'

        self.assertRaises(
            PayPal.InvalidSavedCardIdException,
            lambda: pp.pay_with_saved_card(amount, external_customer_id, saved_card_id)
        )

class VZeroTest(AbstractTest):

    def setUp(self):
        self.shipping_data = {"first_name":"Steve","last_name":"Steverton","street_address":"1 Steve St","extended_address":"Suite 1","locality":"Dover","region":"NH","postal_code":"03820","country_code_alpha2":"US"}
        self.transaction_data = {"amount":"100.00","payment_method_nonce":"FAKE_NONCE"}
        # self.data = self.shipping_data.update(self.transaction_data)

        # uses settings.VZERO_ACCESS_TOKEN by default
        self.vzero = VZero()

    def test_1(self):
        """ test VZeroShipping object """
        shipping = VZeroShipping(data=self.shipping_data)
        self.assertIsNotNone(shipping)

    def test_2(self):
        """ test VZeroTransaction object """

        transaction = VZeroTransaction()
        transaction.update_shipping_data(self.shipping_data)
        transaction.update_transaction_data(self.transaction_data)

    def test_3(self):
        """ try to make the deposit (aka: the braintree 'sale') """
        transaction = VZeroTransaction()
        transaction.update_data(self.shipping_data, self.transaction_data)

        self.assertRaises(VZero.VZeroException,
                          lambda: self.vzero.create_transaction(transaction))
