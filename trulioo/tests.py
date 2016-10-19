#
# tests.py

# from django.test import TestCase
from django.contrib.auth.models import User
from test.classes import AbstractTest
from trulioo.classes import (
    LocationData,
    # CommunicationData,
    NationalIdInfoData,
    PersonInfoData,
    VerifyData,
    Trulioo,
)

#
# Note: these tests assume the settings are configured to use the Draftboard_Demo_Portal account
#       which has configured some test users specific to these tests.


class TestTrulioo(AbstractTest):

    def setUp(self):
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_1(self):
        t = Trulioo()
        data = t.test_connection()
        # print(str(data))

    # def test_2(self):
    #     """ invalid field, or mis formatted fields result in TruliooException """
    #     t = Trulioo()
    #
    #     # the main data class for all params we can pass off to the verify api
    #     verify = VerifyData()
    #     verify.set_field(VerifyData.field_country_code, 'US')
    #
    #     # set an empty PersonInfo object
    #     person = PersonInfoData()
    #     person.set_field(PersonInfoData.field_gender, 'M')
    #     verify.set_data(person)
    #
    #     # set an empty Location object
    #     location = LocationData()
    #     verify.set_data(location)
    #
    #     # CommunicationData objects is where we can set email, mobile number, telephone...
    #     # Try the most basic of verifications by looking up just the email.
    #     communication = CommunicationData()
    #     communication.set_field(CommunicationData.field_email_address, 'admin@draftboard.com')
    #     verify.set_data(communication)
    #
    #     # call the api with the user data weve added to the VerifyData object
    #     # TODO assertRaises( TruliooException, lambda: t.verify(verify) )
    #     data = t.verify(verify)
    #     print('verify() data:', str(data))

    def test_3(self):
        t = Trulioo()
        data = t.test_authentication()
        # print(str(data))

    def test_4(self):
        """
        less than minimum verification (some fields may match, but service gives an overall 'nomatch'):

            First Name, Last Name, Full Name, Year of Birth, Postal Code (5 datapoints total)

        test user: Justin, Williams, 1988, 10001
        """
        t = Trulioo()

        # the main data class for all params we can pass off to the verify api
        verify = VerifyData()
        verify.set_field(VerifyData.field_country_code, 'US')

        # set an empty PersonInfo object
        person = PersonInfoData()
        person.set_field(PersonInfoData.field_first_given_name, 'Justin')
        person.set_field(PersonInfoData.field_first_surname, 'Williams')
        # person.set_field(PersonInfoData.field_gender, 'M')
        # person.set_field(PersonInfoData.field_day_of_birth, 1)
        # person.set_field(PersonInfoData.field_month_of_birth, 1)
        person.set_field(PersonInfoData.field_year_of_birth, 1988)
        verify.set_data(person)

        # Set an empty SSN object
        nationalId = NationalIdInfoData()
        # We only support US SSNs so default to that.
        nationalId.set_field(NationalIdInfoData.field_type, 'SocialService')
        nationalId.set_field(NationalIdInfoData.field_country, 'US')
        nationalId.set_field(NationalIdInfoData.field_number, '000568791')
        verify.set_data(nationalId)

        # set an empty Location object
        location = LocationData()
        location.set_field(LocationData.field_postal_code, '10001')
        verify.set_data(location)

        # CommunicationData objects is where we can set email, mobile number, telephone...
        # Try the most basic of verifications by looking up just the email.
        # communication = CommunicationData()
        # communication.set_field(CommunicationData.field_telephone, '111 222 3333')
        # verify.set_data(communication)

        data = t.verify(verify)
        # print('verify() data:', str(data))

    # def test_5(self):
    #     """
    #     Note: this is not a pure minimum actually, but it verifies the user.
    #     We can actually remove either the birth day/month as long as the street address
    #     is there, or we can remove the street address if the birth day/month are matching.
    #
    #     the minimum fields for verification (most individual fields match,
    #     and the service gives an overall result of verifying the citizen)
    #
    #         First Name,
    #         Last Name,
    #         Day of Birth,
    #         Month of Birth,
    #         Year of Birth,
    #         Street Address (technically its the Street Number, Street Name and Street Type)
    #         Postal(zip) Code,
    #         State
    #
    #     test user:
    #         Justin,
    #         Williams,
    #         1/1/1988,           # birthdate in form: DD/
    #         1 Justin St.         # street address with Number, Name, Type
    #         Justintown           # city
    #         10001               # zipcode
    #     """
    #     t = Trulioo()
    #
    #     # the main data class for all params we can pass off to the verify api
    #     verify = VerifyData()
    #     verify.set_field(VerifyData.field_country_code, 'US')
    #
    #     # set an empty PersonInfo object
    #     person = PersonInfoData()
    #     person.set_field(PersonInfoData.field_first_given_name, 'Justin')
    #     person.set_field(PersonInfoData.field_first_surname, 'Williams')
    #     # person.set_field(PersonInfoData.field_gender, 'M')
    #     person.set_field(PersonInfoData.field_day_of_birth, 4)
    #     person.set_field(PersonInfoData.field_month_of_birth, 8)
    #     person.set_field(PersonInfoData.field_year_of_birth, 1988)
    #     verify.set_data(person)
    #
    #     # set an empty Location object
    #     location = LocationData()
    #     location.set_field(LocationData.field_building_number, '1')
    #     location.set_field(LocationData.field_street_name, 'Justin')
    #     location.set_field(LocationData.field_street_type, 'St')
    #     location.set_field(LocationData.field_city, 'Justintown')
    #     location.set_field(LocationData.field_postal_code, '10001')
    #     location.set_field(LocationData.field_state_province_code, 'TX')
    #     verify.set_data(location)
    #
    #     # CommunicationData objects is where we can set email, mobile number, telephone...
    #     # Try the most basic of verifications by looking up just the email.
    #     # communication = CommunicationData()
    #     # communication.set_field(CommunicationData.field_telephone, '111 222 3333')
    #     # verify.set_data(communication)
    #
    #     data = t.verify(verify)
    #     print('verify() data:', str(data))

    # def test_6(self):
    #     """
    #     minimum info to verify, includes birth day/month but no street address
    #
    #     test user:
    #         Justin,
    #         Williams,
    #         1 / 1 / 1988,       # birthdate in form: MM/DD/YYYY
    #         Justintown           # city
    #         10001               # zipcode
    #         State               # state
    #
    #     """
    #     t = Trulioo()
    #
    #     # the main data class for all params we can pass off to the verify api
    #     verify = VerifyData()
    #     verify.set_field(VerifyData.field_country_code, 'US')
    #
    #     # set an empty PersonInfo object
    #     person = PersonInfoData()
    #     person.set_field(PersonInfoData.field_first_given_name, 'Justin')
    #     person.set_field(PersonInfoData.field_first_surname, 'Williams')
    #     # person.set_field(PersonInfoData.field_gender, 'M')
    #     person.set_field(PersonInfoData.field_day_of_birth, 4)
    #     person.set_field(PersonInfoData.field_month_of_birth, 8)
    #     person.set_field(PersonInfoData.field_year_of_birth, 1988)
    #     verify.set_data(person)
    #
    #     # set an empty Location object
    #     location = LocationData()
    #     # location.set_field(LocationData.field_building_number, '1')
    #     # location.set_field(LocationData.field_street_name, 'Justin')
    #     # location.set_field(LocationData.field_street_type, 'St')
    #     #location.set_field(LocationData.field_city, 'Justintown')
    #     location.set_field(LocationData.field_postal_code, '10001')
    #     #location.set_field(LocationData.field_state_province_code, 'TX')
    #     verify.set_data(location)
    #
    #     data = t.verify(verify)
    #     print('verify() data:', str(data))

    def test_7(self):
        """
        minimum info to verify, includes birth day/month but no street address

        test user:
            Justin,
            Williams,
            x / x / 1988,       # birthdate in form: MM/DD/YYYY
            1 Justin St          # street address with Number, Name, Type
            Justintown           # city
            10001               # zipcode

        """
        t = Trulioo()

        # the main data class for all params we can pass off to the verify api
        verify = VerifyData()
        verify.set_field(VerifyData.field_country_code, 'US')

        # set an empty PersonInfo object
        person = PersonInfoData()
        person.set_field(PersonInfoData.field_first_given_name, 'Justin')
        person.set_field(PersonInfoData.field_first_surname, 'Williams')
        person.set_field(PersonInfoData.field_year_of_birth, 1988)
        verify.set_data(person)

        # Set an empty SSN object
        nationalId = NationalIdInfoData()
        # We only support US SSNs so default to that.
        nationalId.set_field(NationalIdInfoData.field_type, 'SocialService')
        nationalId.set_field(NationalIdInfoData.field_country, 'US')
        nationalId.set_field(NationalIdInfoData.field_number, '000568791')
        verify.set_data(nationalId)

        # set an empty Location object
        location = LocationData()
        location.set_field(LocationData.field_building_number, '420')
        location.set_field(LocationData.field_street_name, '9th')
        location.set_field(LocationData.field_street_type, 'Avenue')
        location.set_field(LocationData.field_city, 'New York')
        location.set_field(LocationData.field_postal_code, '10001')
        location.set_field(LocationData.field_state_province_code, 'NY')
        verify.set_data(location)

        data = t.verify(verify)
        # print('verify() data:', str(data))

    def test_8(self):
        """
        test the method verify_minimal() which takes a basic set of arguments
        and returns a True/False boolean indicating if the user was verified(True) or not (False)
        """

        t = Trulioo()
        verified = t.verify_minimal(
            first='Justin', last='Williams', birth_day=4, birth_month=8, birth_year=1988,
            postal_code='10001', user=self.user, ssn="000568791")
        self.assertTrue(verified)
    #
    # def test_9(self):
    #     """
    #     make sure verify_minimal() create a model Verification as a log of the Trulioo transaction
    #
    #     this test does not include the user, but the production system probably should!
    #     """
    #
    #     t = Trulioo()
    #     verified = t.verify_minimal(
    #       'Justin', 'Williams', 4, 8, 1988, '10001', user=user, ssn="000568791")
    #     self.assertTrue(verified)
    #
    #     # check if a model exists
    #     self.assertIsNotNone(t.verification_model)

    def test_10(self):
        """
        make sure verify_minimal() create a model Verification as a log of the Trulioo transaction

        """
        t = Trulioo()
        verified = t.verify_minimal(
            first='Justin', last='Williams', birth_day=4, birth_month=8, birth_year=1988,
            postal_code='10001', user=self.user, ssn="000568791")
        self.assertTrue(verified)

        # check if a model exists
        self.assertIsNotNone(t.verification_model)
        self.assertIsNotNone(t.verification_model.user)
