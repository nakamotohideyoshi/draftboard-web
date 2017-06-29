# A successful match from the CustomerIdentity/CustomerRegistration endpoint.
CUSTOMER_REGISTRATION_MATCH_RESPONSE = {
    'ApiKey': 'k2m9yX4Tl0WXuz8Ahc5muA',
    'ApiVersion': 3.0,
    'CustomerRegistrationLink': None,
    'FraudConfidenceScore': 96.0,
    'IdentityConfidenceScore': 94.51,
    'LocationDetail': {
        'Altitude': None,
        'ComplianceLocationServiceStatus': 'Inactive',
        'ComplianceLocationStatus': True,
        'IdentifierType': 'IP',
        'IdentifierUsed': '174.51.188.204',
        'Latitude': 39.729,
        'LocationDateTime': '2017-06-28T01:30:43.567',
        'LocationServiceLevel': 'Standard',
        'LocationStatus': 2,
        'Longitude': -104.9528,
        'Radius': None,
        'ReasonCodes': ['LL-GEO-US-CO'],
        'Speed': None
    },
    'MerchantCustomerID': '51--automated_test_user',
    'MerchantID': 'Q2wprL4aKEKEj-dzTu44BA',
    'MerchantSessionID': 'GIDXSB_TODO: this',
    'ProfileMatch': {
        'AddressMatch': False,
        'CitizenshipMatch': True,
        'DateOfBirthMatch': True,
        'EmailMatch': False,
        'IdDocumentMatch': False,
        'MobilePhoneMatch': False,
        'NameMatch': True,
        'PhoneMatch': False
    },
    'ProfileMatches': [],
    'ReasonCodes': ['ID-VERIFIED', 'LL-GEO-US-CO'],
    'ResponseCode': 0,
    'ResponseMessage': 'No error.',
    'WatchChecks': []
}


# NO match from the CustomerIdentity/CustomerRegistration endpoint.
CUSTOMER_REGISTRATION_FAIL_RESPONSE = {
    'ApiKey': 'k2m9yX4Tl0WXuz8Ahc5muA',
    'ApiVersion': 3.0,
    'CustomerRegistrationLink': None,
    'FraudConfidenceScore': 78.0,
    'IdentityConfidenceScore': 0.0,
    'LocationDetail': {
        'Altitude': None,
        'ComplianceLocationServiceStatus': None,
        'ComplianceLocationStatus': False,
        'IdentifierType': None,
        'IdentifierUsed': None,
        'Latitude': None,
        'LocationDateTime': None,
        'LocationServiceLevel': None,
        'LocationStatus': 0,
        'Longitude': None,
        'Radius': None,
        'ReasonCodes': [],
        'Speed': None
    },
    'MerchantCustomerID': '50--automated_test_user',
    'MerchantID': 'Q2wprL4aKEKEj-dzTu44BA',
    'MerchantSessionID': 'GIDXSB_TODO: this',
    'ProfileMatch': {
        'AddressMatch': False,
        'CitizenshipMatch': False,
        'DateOfBirthMatch': False,
        'EmailMatch': False,
        'IdDocumentMatch': False,
        'MobilePhoneMatch': False,
        'NameMatch': False,
        'PhoneMatch': False
    },
    'ProfileMatches': [],
    'ReasonCodes': ['ID-FAIL', 'ID-UNKN'],
    'ResponseCode': 0,
    'ResponseMessage': 'No error.',
    'WatchChecks': []
}

# Failed response due to a improperly-formatted DOB.
CUSTOMER_REGISTRATION_BAD_INPUT_RESPONSE = {
    'ApiKey': 'k2m9yX4Tl0WXuz8Ahc5muA',
    'ApiVersion': 3.0,
    'CustomerRegistrationLink': None,
    'FraudConfidenceScore': 0.0,
    'IdentityConfidenceScore': 0.0,
    'LocationDetail': {
        'Altitude': None,
        'ComplianceLocationServiceStatus': None,
        'ComplianceLocationStatus': False,
        'IdentifierType': None,
        'IdentifierUsed': None,
        'Latitude': None,
        'LocationDateTime': None,
        'LocationServiceLevel': None,
        'LocationStatus': 0,
        'Longitude': None,
        'Radius': None,
        'ReasonCodes': [],
        'Speed': None
    },
    'MerchantCustomerID': '32--dwGwWGoYjZBBBiPAgNwepwlpYXAmXnJWcypxRvd',
    'MerchantID': 'Q2wprL4aKEKEj-dzTu44BA',
    'MerchantSessionID': 'TODO: make this something',
    'ProfileMatch': {
        'AddressMatch': False,
        'CitizenshipMatch': False,
        'DateOfBirthMatch': False,
        'EmailMatch': False,
        'IdDocumentMatch': False,
        'MobilePhoneMatch': False,
        'NameMatch': False,
        'PhoneMatch': False
    },
    'ProfileMatches': [],
    'ReasonCodes': [],
    'ResponseCode': 501,
    'ResponseMessage': 'DateOfBirth supplied is out of range.',
    'WatchChecks': None
}

# A response for a valid identity that has ALREADY been verified by us.
CUSTOMER_REGISTRATION_EXISTING_MATCH_RESPONSE = {
    'MerchantCustomerID': '75--automated_test_user',
    'LocationDetail': {
        'IdentifierType': 'IP',
        'IdentifierUsed': '174.51.188.204',
        'Latitude': 39.729,
        'Longitude': -104.9528,
        'Radius': None,
        'Speed': None,
        'Altitude': None,
        'LocationDateTime': '2017-06-28T01:30:43.567',
        'ComplianceLocationStatus': True,
        'LocationStatus': 2,
        'LocationServiceLevel': 'Standard',
        'ComplianceLocationServiceStatus': 'Inactive',
        'ReasonCodes': ['LL-GEO-US-CO']
    }, 'ProfileMatch': {
        'NameMatch': True,
        'AddressMatch': False,
        'EmailMatch': False,
        'IdDocumentMatch': False,
        'PhoneMatch': False,
        'MobilePhoneMatch': False,
        'DateOfBirthMatch': True,
        'CitizenshipMatch': True
    }, 'CustomerRegistrationLink': None,
    'IdentityConfidenceScore': 93.47,
    'FraudConfidenceScore': 95,
    'WatchChecks': [],
    'ReasonCodes': ['ID-EX', 'ID-VERIFIED', 'LL-GEO-US-CO'],
    'ProfileMatches': [
        '71--automated_test_user',
        '67--automated_test_user',
        '51--automated_test_user'
    ],
    'ApiKey': 'k2m9yX4Tl0WXuz8Ahc5muA',
    'MerchantID': 'Q2wprL4aKEKEj-dzTu44BA',
    'MerchantSessionID': 'GIDXSB_TODO: this',
    'ResponseCode': 0,
    'ResponseMessage': 'No error.',
    'ApiVersion': 3
}
