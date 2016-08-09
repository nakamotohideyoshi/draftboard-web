#
# classes.py

from django.conf import settings
from util.timesince import timeit
import json
import requests

# this allegedly lists some of the required/optional fields of the Normalized API:
#   https://portal.globaldatacompany.com/NormalizedApiGuidelines/Report?configurationName=Identity%20Verification&Country=US

class DataWithSetField(object):

    data = None # child class will override this dict
    def set_field(self, field, obj):

        self.data[field] = obj

class LocationData(DataWithSetField): # TODO - finish implementing

    field = 'Location'

    def __init__(self):
        self.data = {

        }

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
            self.field_mobile_number : "",        # string
            self.field_telephone : "",            # string
            self.field_email_address : "",        # string
        }

class PersonInfoData(DataWithSetField):
    """
    for more info:

        https://api.globaldatacompany.com/Help/ResourceModel?modelName=PersonInfo

    """
    field = 'PersonInfo'

    field_first_given_name = 'FirstGivenName'               # first name OR initial
    field_middle_name = 'MiddleName'                        # first name OR initial
    field_first_surname = 'FirstSurName'
    field_second_surname = 'SecondSurname'
    field_iso_latin1_name = 'ISOLatin1Name'
    field_day_of_birth = 'DayOfBirth' # integer
    field_month_of_birth = 'MonthOfBirth' # integer
    field_year_of_birth = 'YearOfBirth' # integer
    field_minimum_age = 'MinimumAge' # integer
    field_gender = 'Gender'                                 # Single character M / F
    field_additional_fullname = 'FullName'

    def __init__(self):
        self.data = {
            self.field_first_given_name: '',            # "sample string 1",
            self.field_middle_name: '',                 #  "sample string 2",
            self.field_first_surname: '',               #  "sample string 3",
            self.field_second_surname: '',              #  "sample string 4",
            self.field_iso_latin1_name: '',             #  "sample string 5",
            self.field_day_of_birth: 0, #  ,
            self.field_month_of_birth: 0, #  ,
            self.field_year_of_birth: 0, #  ,
            self.field_minimum_age: 0, #  ,
            self.field_gender: '',                      # "sample string 6",
            "AdditionalFields": {
                self.field_additional_fullname : '',    # "sample string 1"
            }
        }

class VerifyData(DataWithSetField):
    """
    data class that helps build the json object to pass to the verify api

    more info:

        https://api.globaldatacompany.com/Help/Api/POST-verifications-v1-verify

    """

    class VerifyDataValidationError(Exception): pass

    field_accept_terms = 'AcceptTruliooTermsAndConditions'
    field_demo = 'Demo'
    field_cleansed_address = 'CleansedAddress'
    field_configuration_name = 'ConfigurationName'
    field_consent_for_data_sources = 'ConsentForDataSources'
    field_country_code = 'CountryCode'
    field_data_fields = 'DataFields'     # dict containing all the granular data points about the user

    required_data_fields_subfields = [
        PersonInfoData.field,
        LocationData.field,
        CommunicationData.field,
    ]

    def __init__(self):
        self.data = {
            self.field_accept_terms: True,
            self.field_demo: True,
            self.field_cleansed_address: True,
            #self.field_configuration_name: '', # string, Default value will be 'Identity Verification'
            self.field_consent_for_data_sources : [
                # "sample string 1",
                # "sample string 2"
            ],
            self.field_country_code : None,       # "sample string 6",
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
        self.validate() # raise validation errors if we havent set the object up with enough user info
        return self.data

    def validate(self):
        """
        we know certain fields are expected, and this will
        raise TruliooValidationError in case we can error
        before even attempting to make an api call we know will not work
        """
        data_fields = self.data.get(self.field_data_fields)
        if data_fields is None or data_fields == {}:
            raise self.VerifyDataValidationError(self.field_data_fields + ' is None or empty {}')

        for f in self.required_data_fields_subfields:
            if self.data[self.field_data_fields].get(f) is None:
                raise self.VerifyDataValidationError(f + ' must be set! it was None.')

class Trulioo(object):
    """
    Used to access the Trulioo service to perform user identity confirmation.
    This service is primarily used when a new user attempts to create an account,
    because we want to confirm they are a real person.

    for more info, see:

        https://api.globaldatacompany.com/Help

    """

    class TruliooException(Exception): pass # TODO - be more specific once we know the types of errors(?)

    # TODO - eventually we will want to default to False here
    demo = True # the verification will be matched against pre-configured entities and not charged to customer

    trulioo_user = settings.TRULIOO_USER
    trulioo_password = settings.TRULIOO_PASSWORD

    headers = {"Content-Type": "application/json; charset=utf-8"}
    auth = (trulioo_user, trulioo_password)

    api_base_url = settings.TRULIOO_API_BASE_URL

    url_test_connection = '/connection/v1/sayhello/draftboard'      # GET
    url_test_authentication = '/connection/v1/testauthentication'   # GET
    url_verify = '/verifications/v1/verify'                         # POST

    def __init__(self):
        self.session = requests.Session()
        self.r = None  # save the last server response

    def build_url(self, endpoint):
        return '%s%s' % (self.api_base_url, endpoint)

    def r_to_json(self, r):
        j = json.loads(r.text)
        return j

    @timeit
    def call(self, url, data):
        """ POST some data to a Trulioo api and return the contents of the response as json """
        print('url:    ', str(url))
        print('headers:', str(self.headers))
        print('auth:   ', str(self.auth))
        self.r = self.session.post(url, json.dumps(data), headers=self.headers, auth=self.auth)
        print('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def test_connection(self):
        """ authentication not required - basically ping the api with an http GET """
        url = self.build_url(self.url_test_connection)
        self.r = self.session.get(url)
        print('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def test_authentication(self):
        url = self.build_url(self.url_test_authentication)
        self.r = self.session.get(url, auth=self.auth)
        print('http status [%s]' % (str(self.r.status_code)))
        return self.r_to_json(self.r)

    def verify(self, verify_obj):
        """
        validate the user based on the email they are using to create an account.
        if the user can create an account, this method will simply do nothing,
        and no exceptions will be raised.

        exceptions will be thrown if the user is not able to be validated/green-lighted.

        :param DataFields:
        """

        data = verify_obj.get_data()

        print('verify_obj.data:', str(data))

        url = self.build_url(self.url_verify)
        response = self.call(url, data)
        if isinstance(response, str):
            err_msg = 'api error: %s' % response
            print(err_msg)
            raise self.TruliooException(err_msg)

        errors1 = response.get('ModelState')
        if errors1 is not None:
            raise self.TruliooException(str(errors1))

        # potential response (as json):
        # {'Message': 'The request is invalid.',
        #  'ModelState': {'request': ['Unknown property email']}}
        return response # as json