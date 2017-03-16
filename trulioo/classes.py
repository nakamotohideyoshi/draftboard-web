#
# classes.py

import json
import logging

import requests
from django.conf import settings

from trulioo.models import Verification
from util.timesince import timeit

logger = logging.getLogger('trulioo.classes')


# this allegedly lists some of the required/optional fields of the Normalized API:
#   https://portal.globaldatacompany.com/NormalizedApiGuidelines/Report?configurationName=Identity%20Verification&Country=US


class DataWithSetField(object):
    data = None  # child class will override this dict

    def set_field(self, field, obj):
        self.data[field] = obj


class LocationData(DataWithSetField):
    """
    more info:  https://api.globaldatacompany.com/Help/ResourceModel?modelName=Location
    """

    field = 'Location'

    field_building_number = 'BuildingNumber'  # house/civic/builing number of home address
    field_building_name = 'BuildingName'  # name of the building of home address
    field_unit_number = 'UnitNumber'  # flat/unit/apt number of home address
    field_street_name = 'StreetName'  # street name of primary residence
    field_street_type = 'StreetType'  # 'St', 'Rd', etc...
    field_city = 'City'  # city of home address
    field_suburb = 'Suburb'  # suburb/subdivision/municipality of home address
    field_county = 'County'  # county/district of home address
    field_state_province_code = 'StateProvinceCode'  # for UnitedStates, expected 2 character code
    field_country = 'Country'  # country of physical address (ISO 3166-1 alpha-2 code)
    field_postal_code = 'PostalCode'  # zip code or postal code of home address
    field_additional_fields = 'AdditionalFields'  # not usually used

    def __init__(self):
        self.data = {}


class CommunicationData(DataWithSetField):
    """
    by default, all valid fields are initialized with empty strings
    because the api does not seem to appreciate null values if
    the programmer does not set everything.
    """

    field = 'Communication'

    field_mobile_number = 'MobileNumber'
    field_telephone = 'Telephone'
    field_email_address = 'EmailAddress'

    def __init__(self):
        self.data = {
            self.field_mobile_number: "",  # string
            self.field_telephone: "",  # string
            self.field_email_address: "",  # string
        }


class PersonInfoData(DataWithSetField):
    """
    for more info:

        https://api.globaldatacompany.com/Help/ResourceModel?modelName=PersonInfo

    """
    field = 'PersonInfo'

    field_first_given_name = 'FirstGivenName'  # first name OR initial
    field_middle_name = 'MiddleName'  # first name OR initial
    field_first_surname = 'FirstSurName'
    field_second_surname = 'SecondSurname'
    field_iso_latin1_name = 'ISOLatin1Name'
    field_day_of_birth = 'DayOfBirth'  # integer
    field_month_of_birth = 'MonthOfBirth'  # integer
    field_year_of_birth = 'YearOfBirth'  # integer
    field_minimum_age = 'MinimumAge'  # integer
    field_gender = 'Gender'  # Single character M / F
    field_additional_fullname = 'FullName'

    def __init__(self):
        self.data = {
            # self.field_first_given_name: '',            # "sample string 1",
            # self.field_middle_name: '',                 #  "sample string 2",
            # self.field_first_surname: '',               #  "sample string 3",
            # self.field_second_surname: '',              #  "sample string 4",
            # self.field_iso_latin1_name: '',             #  "sample string 5",
            # self.field_day_of_birth: 0, #  ,
            # self.field_month_of_birth: 0, #  ,
            # self.field_year_of_birth: 0, #  ,
            # self.field_minimum_age: 0, #  ,
            # self.field_gender: '',                      # "sample string 6",
            # "AdditionalFields": {
            #     self.field_additional_fullname : '',    # "sample string 1"
            # }
        }


class VerifyDataValidationError(Exception):
    pass


class VerifyData(DataWithSetField):
    """
    data class that helps build the json object to pass to the verify api

    more info:

        https://api.globaldatacompany.com/Help/Api/POST-verifications-v1-verify

    """

    field_accept_terms = 'AcceptTruliooTermsAndConditions'
    field_demo = 'Demo'
    field_cleansed_address = 'CleansedAddress'
    field_configuration_name = 'ConfigurationName'
    field_consent_for_data_sources = 'ConsentForDataSources'
    field_country_code = 'CountryCode'
    field_data_fields = 'DataFields'  # dict containing all the granular data points about the user

    required_data_fields_subfields = [
        PersonInfoData.field,
        LocationData.field,
        CommunicationData.field,
    ]

    def __init__(self):
        self.data = {
            self.field_accept_terms: True,
            self.field_demo: settings.TRULIOO_DEMO_MODE,
            self.field_cleansed_address: True,
            # self.field_configuration_name: '', # string, Default value will be
            # 'Identity Verification'
            self.field_consent_for_data_sources: [
                # "sample string 1",
                # "sample string 2"
            ],
            self.field_country_code: None,  # "sample string 6",
            self.field_data_fields: {},

            #
            # used fields (by us, potentially)
            # "PersonInfo": { ... },
            # "Location": { ... },
            # "Communication: { ... },

            #
            # un-used other fields for the data for this api:
            # "DriverLicence": { ... },
            # "NationalIds": [ { ... }, ..., { ... } ], # list of dicts
            # "Passport": { ... },
        }

    def set_data(self, data_obj):
        self.data[self.field_data_fields][data_obj.field] = data_obj.data

    def get_data(self):
        self.validate()  # raise validation errors if we havent set the object up with enough info
        return self.data

    def validate(self):
        """
        we know certain fields are expected, and this will
        raise TruliooValidationError in case we can error
        before even attempting to make an api call we know will not work
        """
        data_fields = self.data.get(self.field_data_fields)
        if data_fields is None or data_fields == {}:
            raise VerifyDataValidationError(self.field_data_fields + ' is None or empty {}')

            # for f in self.required_data_fields_subfields:
            #     if self.data[self.field_data_fields].get(f) is None:
            #         raise self.VerifyDataValidationError(f + ' must be set! it was None.')


class TruliooResponse(object):
    field_record = 'Record'
    field_transaction_id = 'TransactionID'
    field_record_status = 'RecordStatus'
    field_transaction_record_id = 'TransactionRecordID'

    def __init__(self, data):
        self.data = data
        self.record = self.data.get(self.field_record, {})

    def get_record_status(self):
        # returns 'nomatch' or 'match'
        record_status = self.record.get(self.field_record_status)
        return record_status

    def get_transaction(self):
        return self.data.get(self.field_transaction_id)

    def get_transaction_record(self):
        return self.record.get(self.field_transaction_record_id)

    def get_errors(self):
        return self.record.get('Errors', [])


class TruliooException(Exception):
    pass  # TODO - be more specific once we know the types of errors(?)


class Trulioo(object):
    """
    Used to access the Trulioo service to perform user identity confirmation.
    This service is primarily used when a new user attempts to create an account,
    because we want to confirm they are a real person.

    for more info, see:

        https://api.globaldatacompany.com/Help

    """

    # the api ultimately returns 'match' or 'nomatch'.
    # 'match' indicates the person was verified successfully and is a real person.
    verification_status_match = 'match'

    # the default country to use in the name/address verification,
    # particularly verify(), verify_minimal() methods
    default_country = 'US'

    # TODO - eventually we will want to default to False here
    demo = settings.TRULIOO_DEMO_MODE

    trulioo_user = settings.TRULIOO_USER
    trulioo_password = settings.TRULIOO_PASSWORD

    headers = {"Content-Type": "application/json; charset=utf-8"}
    auth = (trulioo_user, trulioo_password)

    api_base_url = settings.TRULIOO_API_BASE_URL

    url_test_connection = '/connection/v1/sayhello/draftboard'  # GET
    url_test_authentication = '/connection/v1/testauthentication'  # GET
    url_verify = '/verifications/v1/verify'  # POST
    user = None

    def __init__(self, user=None):
        self.session = requests.Session()
        self.r = None  # save the last server response
        self.response_json = None
        self.verification_model = None
        self.user = user

    def build_url(self, endpoint):
        return '%s%s' % (self.api_base_url, endpoint)

    @staticmethod
    def r_to_json(r):
        j = json.loads(r.text)
        return j

    @timeit
    def call(self, url, data):
        """ POST some data to a Trulioo api and return the contents of the response as json """
        logger.debug('url:    ', str(url))
        logger.debug('headers:', str(self.headers))
        logger.debug('auth:   ', str(self.auth))
        self.r = self.session.post(url, json.dumps(data), headers=self.headers, auth=self.auth)
        logger.debug('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def test_connection(self):
        """ authentication not required - basically ping the api with an http GET """
        url = self.build_url(self.url_test_connection)
        self.r = self.session.get(url)
        logger.debug('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def test_authentication(self):
        url = self.build_url(self.url_test_authentication)
        self.r = self.session.get(url, auth=self.auth)
        logger.debug('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def verify(self, verify_obj):
        """
        validate the user based on the email they are using to create an account.
        if the user can create an account, this method will simply do nothing,
        and no exceptions will be raised.

        exceptions will be thrown if the user is not able to be validated/green-lighted.

        returns the entire JSON response from the verification API
        """

        data = verify_obj.get_data()

        # build the api url and call it, getting a JSON message back as the response
        url = self.build_url(self.url_verify)
        response = self.call(url, data)

        # check the response for errors
        if isinstance(response, str):
            err_msg = 'Trulioo API error: %s' % response
            logger.warning(err_msg)
            raise TruliooException(err_msg)
        errors1 = response.get('ModelState')
        if errors1 is not None:
            raise TruliooException(str(errors1))

        # check the various parts of the response for errors
        # record = response.get('Record', {})
        # record_status = record.get('RecordStatus') # returns 'nomatch' or 'match'
        # logger.info('RecordStatus:', record_status)
        tr = TruliooResponse(response)
        # record_status = tr.get_record_status()

        # raise the first error found
        record_errors = tr.get_errors()
        for record_error in record_errors:
            message = record_error.get('Message')
            raise TruliooException(message)

        # return the json response
        return response

    def verify_minimal(self, first, last, birth_day, birth_month, birth_year,
                       postal_code, country_code=None, user=None):
        """
        verify a user based on the given information, using Trulioo.

        returns a boolean indicating if the user was successfully matched/verified (True) or not
        (False)

        :param first: string first name
        :param last: string last name
        :param birth_day: integer between 1 and 31 inclusive
        :param birth_month: integer between 1 and 12 inclusive
        :param birth_year: integer 4 digit year
        :param postal_code: string zip/postal code (must be string to capture leading 0's)
        :param country_code: optionally specify the country. default: 'US'
        :param user: optionally specify the django user which will cause the backend to save the
            transaction ids
        :return: boolean indicating Trulioo Verification success. True => match, False => nomatch
            (failure to verify)
        """

        country = country_code
        if country is None:
            country = self.default_country

        verify = VerifyData()
        verify.set_field(VerifyData.field_country_code, country)

        # set an empty PersonInfo object
        person = PersonInfoData()
        person.set_field(PersonInfoData.field_first_given_name, first)
        person.set_field(PersonInfoData.field_first_surname, last)
        person.set_field(PersonInfoData.field_day_of_birth, birth_day)
        person.set_field(PersonInfoData.field_month_of_birth, birth_month)
        person.set_field(PersonInfoData.field_year_of_birth, birth_year)
        verify.set_data(person)

        # set an empty Location object
        location = LocationData()
        location.set_field(LocationData.field_postal_code, postal_code)
        verify.set_data(location)

        # verify the person using primary verify method
        self.response_json = self.verify(verify)
        # logger.info(self.response_json)

        tr = TruliooResponse(self.response_json)
        record_status = tr.get_record_status()

        if user:
            logger.debug('saving identity varification for user: %s', user)
            # if the user was passed in, then save a Verification model instance of
            # this verification
            self.verification_model = self.save_verification(user, tr)
        else:
            logger.debug('no User was supplied, not saving identity varification at this time.')

        # return the success of failure of the verification
        # 'match' indicates success
        return record_status == self.verification_status_match

    @staticmethod
    def save_verification(user, trulioo_response):
        transaction = trulioo_response.get_transaction()  # its a string identifier
        transaction_record = trulioo_response.get_transaction_record()  # its a string identifier
        record_status = trulioo_response.get_record_status()

        logger.info('Saving identity verification for user: %s' % user)
        v = Verification.objects.create(
            user=user, transaction=transaction, transaction_record=transaction_record,
            record_status=record_status)
        return v
