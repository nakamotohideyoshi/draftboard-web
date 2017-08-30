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

# Failed response due to a improperly-formatted DOB. - 200 status code.
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


# 500 status code
SERVICE_ERROR_RESPONSE = {
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
    'MerchantCustomerID': 'TEST--173--automated_test_user',
    'MerchantID': 'Q2wprL4aKEKEj-dzTu44BA',
    'MerchantSessionID': 'GIDXSB_8b4f0dbb-76b9-41db-9eea-7eb3cfa41ee3',
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
    'ResponseCode': 500,
    'ResponseMessage': 'General application error.',
    'WatchChecks': None
}


WEB_REG_SUCCESS_RESPONSE = {
    "SessionID": "c-duZaP4WkCIiZ2sMgWx-Q",
    "SessionURL": "%3cdiv+data-gidx-script-loading%3d%27true%27%3eLoading...%3c%2fdiv%3e%3cscript+src%3d%27https%3a%2f%2fws.gidx-service.in%2fv3.0%2fWebSession%2fRegistration%3fsessionid%3dc-duZaP4WkCIiZ2sMgWx-Q%27+data-tsevo-script-tag+data-gidx-session-id%3d%27c-duZaP4WkCIiZ2sMgWx-Q%27+type%3d%27text%2fjavascript%27%3e%3c%2fscript%3e",
    "SessionExpirationTime": "2017-07-07T23:41:00.89Z",
    "SessionScore": 49,
    "ReasonCodes": [],
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "MerchantSessionID": "GIDXSB_36ed8b29-2d48-49a4-94a3-6b8d8135cb26",
    "ResponseCode": 0,
    "ResponseMessage": "No error.",
    "ApiVersion": 3
}

# If we have previously verified this person, but reqeust a webreg embed, we'll get an
# `ID-VERIFIED` and a script embed.
# TODO: setup a test case for this. The only reason this would happen is if we verified a user,
# then removed the Identity or set Identity.status to False afterwards.
WEB_REG_SUCCESS_RESPONSE_ALREADY_VERIFIED = {
  "SessionExpirationTime": "2017-07-13T20:56:15.447Z",
  "ApiVersion": 3,
  "MerchantSessionID": "d56e41c8-504c-437c-bde9-3e65478fb7af",
  "SessionID": "yQZTImyPoUqhhXVlJCoilQ",
  "SessionURL": "%3cdiv+data-gidx-script-loading%3d%27true%27%3eLoading...%3c%2fdiv%3e%3cscript+src%3d%27https%3a%2f%2fws.gidx-service.in%2fv3.0%2fWebSession%2fRegistration%3fsessionid%3dyQZTImyPoUqhhXVlJCoilQ%27+data-tsevo-script-tag+data-gidx-session-id%3d%27yQZTImyPoUqhhXVlJCoilQ%27+type%3d%27text%2fjavascript%27%3e%3c%2fscript%3e",
  "ResponseMessage": "No error.",
  "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
  "SessionScore": 75,
  "ResponseCode": 0,
  "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
  "ReasonCodes": [
    "ID-VERIFIED"
  ]
}


# WebReg callback webhooks.
WEBHOOK_COMPLETE = {
  "StatusCode": 0,
  "SessionID": "UwMM1ZlLLUezFI410B6ZGg",
  "MerchantSessionID": "GIDXSB_9c59b4f7-285f-4e14-8b67-a67e8435f426",
  "SessionScore": 50,
  "ReasonCodes": [],
  "ServiceType": "Customer Registration",
  "StatusMessage": "Registration Complete."
}

WEBHOOK_INELIGIBLE = {
    "StatusCode": 1,
    "SessionID": "UwMM1ZlLLUezFI410B6ZGg",
    "MerchantSessionID": "GIDXSB_9c59b4f7-285f-4e14-8b67-a67e8435f426",
    "SessionScore": 50,
    "ReasonCodes": [

    ],
    "ServiceType": "Customer Registration",
    "StatusMessage": "Customer Ineligible."
}

WEBHOOK_INCOMPLETE = {
  "StatusCode": 2,
  "SessionID": "GP7u13x6Qk2EMFd9qJ9Q4w",
  "MerchantSessionID": "e0a8cd91-133b-4dcc-8567-91753c1b102a",
  "SessionScore": 38,
  "ReasonCodes": [
    "DFP-IPNM",
    "ID-FAIL",
    "ID-UNKN"
  ],
  "ServiceType": "Customer Registration",
  "StatusMessage": "Registration Incomplete. Last reached step is the ID validation page."
}

WEBHOOK_TIMEOUT = {
  "StatusCode": 3,
  "SessionID": "UwMM1ZlLLUezFI410B6ZGg",
  "MerchantSessionID": "GIDXSB_9c59b4f7-285f-4e14-8b67-a67e8435f426",
  "SessionScore": 50,
  "ReasonCodes": [

  ],
  "ServiceType": "Customer Registration",
  "StatusMessage": "Registration Timeout."
}

# This one might be bogus.
WEBHOOK_USER_EXISTS = {
    "results": """
        {
            "StatusCode": 0,
            "SessionID": "bivbLEzRXEa5znJWTkoS0Q",
            "MerchantSessionID": "bcac1b5b-5090-44cf-83ee-4cf752b87b26",
            "SessionScore": 97,
            "ReasonCodes": [
            "DFP-IPNM",
            "ID-EX",
            "ID-PASS",
            "ID-VERIFIED"
            ],
            "ServiceType": "Customer Registration",
            "StatusMessage": "Registration is complete. Please call CustomerRegistration method..."
        }
        """,
}


# This is fake json, should I make it a python object?? whatever.
STATUS_REQUEST = {
    "ReasonCodes": [
        "DFP-IPNM",
        "ID-EX",
        "ID-PASS",
        "ID-VERIFIED"
    ],
    "ResponseMessage": "No error.",
    "ApiVersion": 3,
    "MerchantSessionID": "e6b5fbf4-273d-4dab-a811-8f6ba5d8c7fb",
    "SessionStatusMessage": "Registration is complete. Please call CustomerRegistration method to get registration details.",
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "SessionScore": 95,
    "SessionStatusCode": "0",
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
    "ResponseCode": 0,
    "LocationDetail": {
        "IdentifierUsed": "172.18.0.1",
        "LocationStatus": 0,
        "Longitude": 'null',
        "IdentifierType": "IP",
        "Latitude": 'null',
        "ReasonCodes": [

        ],
        "Radius": 'null',
        "Speed": 'null',
        "LocationDateTime": "2017-06-29T19:48:38.45",
        "ComplianceLocationServiceStatus": "Passive",
        "ComplianceLocationStatus": 'false',
        "LocationServiceLevel": "Auto",
        "Altitude": 'null'
    }
}


WEB_CASHIER_CREATE_SESSION = {
  "action": "WEB_CACHIER_CREATE_SESSION_REQUEST",
  "request": {
    "ActivityTypeID": "FyP1fg_WkU60JnuIarfOQw",
    "MerchantCustomerID": "TEST--dan--000000000057",
    "ProductTypeID": "iiXXab0LtUCUdZ_6vcdtvQ",
    "CallbackURL": "http://a032f89c.ngrok.io/api/account/identity-webhook/",
    "DeviceTypeID": "2bDPorOkPkepDd8-6Fydtw",
    "MerchantSessionID": "f8884ba4-610f-4fda-8fd9-507693dffccc",
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "MerchantOrderID": "todo",
    "MerchantTransactionID": "todo",
    "CustomerIpAddress": "172.18.0.1",
    "PayActionCode": "PAY",
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA"
  },
  "response": {
    "ResponseMessage": "No error.",
    "SessionURL": "%3cdiv+data-gidx-script-loading%3d%27true%27%3eLoading...%3c%2fdiv%3e%3cscript+src%3d%27https%3a%2f%2fws.gidx-service.in%2fv3.0%2fWebSession%2fCashier%3fsessionid%3d5FwmaKgpiEioTDyXyldkRg%27+data-tsevo-script-tag+data-gidx-session-id%3d%275FwmaKgpiEioTDyXyldkRg%27+type%3d%27text%2fjavascript%27%3e%3c%2fscript%3e",
    "SessionExpirationTime": "2017-08-28T19:22:38.9502224Z",
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
    "ReasonCodes": [
      "LL-UNKN"
    ],
    "MerchantSessionID": "f8884ba4-610f-4fda-8fd9-507693dffccc",
    "SessionID": "5FwmaKgpiEioTDyXyldkRg",
    "ApiVersion": 3,
    "SessionScore": 50,
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "ResponseCode": 0
  },
  "url": "https://api.gidx-service.in/v3.0/api/WebCashier/CreateSession"
}


# Callback - WebCashier example from their documentation.
WEB_CASHIER_CALLBACK = {
    "StatusCode": 0,
    "StatusMessage": "Registration is complete. Please call CustomerRegistration method to get registration details.",
    "SessionID": "X9XeW5FvCEKimOKw59GNPA",
    "MerchantSessionID": "123_ID_GOES_HERE",
    "SessionScore": 96.2,
    "ReasonCodes": ["ID-VERIFIED", "LL-GEO-US-TX", "DFP-VPRP-CORP"],
    "MerchantTransactionID": "1113201405343_1",
    "TransactionStatusCode": 0,
    "TransactionStatusMessage": "Pending",
    "ServiceType": "Payment"
}

# a webhook from the web cachier app for when a user tries to deposit but has not yet
# completed identity verification (I think we will not be allowing users to attempt to
# deposit if they have not yet verified, so this should not happen)
WEB_CASHIER_CALLBACK_PENDING_UNVERIFIED_IDENTITY = {
    "SessionID": "9tskb__mD0CGwvdmadVzSw",
    "MerchantTransactionID": "a50d95ec-041b-4d77-bbcd-57d0130c3e60",
    "MerchantSessionID": "ed5cc90d-2e85-42c8-9fa8-eb7a138cb21b",
    "StatusCode": 0,
    "SessionScore": 51,
    "TransactionStatusCode": 0,
    "ReasonCodes": [
      "DFP-IPNM",
      "LL-UNKN"
    ],
    "TransactionStatusMessage": "Pending",
    "ServiceType": "Payment",
    "StatusMessage": "Payment Session is Complete."
}

# After a deposit transaction has been completed succesfully.
WEB_CASHIER_CALLBACK_SUCCESS = {
  "MerchantTransactionID": "d191369c-290d-46af-94f3-d7b0db45ab09",
  "TransactionStatusCode": 1,
  "TransactionStatusMessage": "Complete",
  "StatusCode": 0,
  "SessionID": "YBlhlLkJ6US9-D50Ihvsnw",
  "MerchantSessionID": "2347cfaa-5e14-44b8-8d0d-5aee5619101a",
  "SessionScore": 77,
  "ReasonCodes": [
    "DFP-IPNM",
    "ID-VERIFIED",
    "LL-UNKN"
  ],
  "ServiceType": "Payment",
  "StatusMessage": "Payment Session is Complete."
}

WEB_CACHIER_PAYMENT_DETAIL_REQUEST = {
  "url": "https://api.gidx-service.in/v3.0/api/WebCashier/PaymentDetail",
  "response": {
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "PaymentDetails": [

    ],
    "MerchantSessionID": "72efc679-986a-4532-a00c-37cfb8fd1b3a",
    "ApiVersion": 3,
    "MerchantTransactionID": "d191369c-290d-46af-94f3-d7b0db45ab09",
    "ResponseCode": 0,
    "ResponseMessage": "No error.",
    "FinancialConfidenceScore": 50
  },
  "action": "WEB_CACHIER_PAYMENT_DETAIL_REQUEST",
  "request": {
    "ApiKey": "k2m9yX4Tl0WXuz8Ahc5muA",
    "MerchantID": "Q2wprL4aKEKEj-dzTu44BA",
    "ProductTypeID": "iiXXab0LtUCUdZ_6vcdtvQ",
    "DeviceTypeID": "2bDPorOkPkepDd8-6Fydtw",
    "MerchantTransactionID": "d191369c-290d-46af-94f3-d7b0db45ab09",
    "ActivityTypeID": "FyP1fg_WkU60JnuIarfOQw",
    "MerchantSessionID": "72efc679-986a-4532-a00c-37cfb8fd1b3a"
  }
}
