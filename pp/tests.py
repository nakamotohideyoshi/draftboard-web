from test.classes import AbstractTest
from pp.classes import (
    VZero,
    VZeroShipping,
    VZeroTransaction,
)


class VZeroTest(AbstractTest):

    def setUp(self):
        self.shipping_data = {
            "first_name": "Steve", "last_name": "Steverton", "street_address": "1 Steve St",
            "extended_address": "Suite 1", "locality": "Dover", "region": "NH",
            "postal_code": "03820", "country_code_alpha2": "US"}
        self.transaction_data = {"amount": "100.00", "payment_method_nonce": "FAKE_NONCE"}
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

        self.assertRaises(
            VZeroTransaction.ValidationError,
            lambda: transaction.update_data(self.shipping_data, self.transaction_data))
