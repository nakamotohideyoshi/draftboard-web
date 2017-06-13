# Action Types used for UserLogs
LOCATION_VERIFY = 0
CONTEST = 1
FUNDS = 2
AUTHENTICATION = 3

TYPES = (
    (LOCATION_VERIFY, 'Location verification'),
    (CONTEST, 'Contest actions'),
    (FUNDS, 'User funds actions'),
    (AUTHENTICATION, 'User authentication'),
)


# User Actions used for UserLogs
IP_CHECK_FAILED_COUNTRY = 0
IP_CHECK_FAILED_STATE = 1
IP_CHECK_FAILED_VPN = 2
IP_CHECK_STATUS = 3
IP_CHECK_LOCAL = 4
LOGIN = 5
LINEUP_CREATED = 6
LINEUP_EDIT = 7
CONTEST_ENTERED = 8
CONTEST_DEREGISTERED = 9
DEPOSIT = 10
DEPOSIT_CLIENT_TOKEN = 11
WITHDRAWAL_PAYPAL = 12
IDENTITY_VERIFICATION_FAILED = 13
IDENTITY_VERIFICATION_SUCCESS = 14
IDENTITY_VERIFICATION_EXISTS = 15
IP_CHECK_UNKNOWN = 16

ACTIONS = (
    (IP_CHECK_FAILED_COUNTRY, 'Country check failed'),
    (IP_CHECK_FAILED_STATE, 'State check failed'),
    (IP_CHECK_FAILED_VPN, 'VPN check failed'),
    (IP_CHECK_STATUS, 'IP check status'),
    (IP_CHECK_LOCAL, 'IP check bypassed, user on local network'),
    (LOGIN, 'User Login'),
    (LINEUP_CREATED, 'Lineup creation'),
    (LINEUP_EDIT, 'Lineup edited'),
    (CONTEST_ENTERED, 'Contest entered'),
    (CONTEST_DEREGISTERED, 'Contest deregistered'),
    (DEPOSIT, 'Deposit funds'),
    (DEPOSIT_CLIENT_TOKEN, 'Deposit pageview'),
    (WITHDRAWAL_PAYPAL, 'Withdraw request - paypal'),
    (IDENTITY_VERIFICATION_FAILED, 'Trulioo verification failed'),
    (IDENTITY_VERIFICATION_SUCCESS, 'Trulioo verification success'),
    (IDENTITY_VERIFICATION_EXISTS, 'User identity is already claimed'),
    (IP_CHECK_UNKNOWN, 'IP not found in the db'),
)
