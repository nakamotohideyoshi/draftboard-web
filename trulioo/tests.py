#
# tests.py

from django.test import TestCase
from test.classes import AbstractTest
from trulioo.classes import (
    LocationData,
    CommunicationData,
    PersonInfoData,
    VerifyData,
    Trulioo,
)

class TestTrulioo(AbstractTest):

    def setUp(self):
        pass # setup anything that the test methods will all use

    def test_1(self):
        t = Trulioo()
        data = t.test_connection()
        print(str(data))

    def test_2(self):

        t = Trulioo()

        # the main data class for all params we can pass off to the verify api
        verify = VerifyData()
        verify.set_field(VerifyData.field_country_code, 'US')

        # set an empty PersonInfo object
        person = PersonInfoData()
        person.set_field(PersonInfoData.field_gender, 'M')
        verify.set_data(person)

        # set an empty Location object
        location = LocationData()
        verify.set_data(location)

        # CommunicationData objects is where we can set email, mobile number, telephone...
        # Try the most basic of verifications by looking up just the email.
        communication = CommunicationData()
        communication.set_field(CommunicationData.field_email_address, 'admin@draftboard.com')
        verify.set_data(communication)

        # call the api with the user data weve added to the VerifyData object
        data = t.verify(verify)
        print('verify() data:', str(data))

    def test_3(self):
        t = Trulioo()
        data = t.test_authentication()
        print(str(data))