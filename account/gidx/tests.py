from django.contrib.auth.models import User
from django.test import TestCase
from model_mommy import mommy

from .exceptions import (ResponseMessageException)
from .request import CustomerRegistrationRequest


class TestCustomerRegistrationRequest(TestCase):
    def setUp(self):
        self.user = mommy.make(
            User,
            username="automated_test_user",
            email="me@zacharywood.com"
        )

    def tearDown(self):
        self.user.delete()

    def test_request(self):
        crr = CustomerRegistrationRequest(
            user=self.user,
            first_name='zachary',
            last_name='wood',
            date_of_birth='02/23/1984',
            ip_address='174.51.188.204'
        )

        print(crr.params)
        crr.get()
        response = crr.res_payload

    # def test_response_message_exception(self):
    #     crr = CustomerRegistrationRequest(
    #         user=self.user,
    #         first_name='zachary',
    #         last_name='wood',
    #         # This is a bad DOB
    #         date_of_birth='02/23/19',
    #         ip_address='174.51.188.204'
    #     )
    #
    #     self.assertRaises(ResponseMessageException, crr.get())
