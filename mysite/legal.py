# All US States
ALL_STATES = [
    'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN',
    'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
    'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA',
    'WI', 'WV', 'WY']

# States we cannot operate in.
BLOCKED_STATES = [
    'AL',
    'AZ',
    'DE',
    'FL',
    'GA',
    'HI',
    'IA',
    'ID',
    'IL',
    'IN',
    'LA',
    'MO',
    'MT',
    'NV',
    'TX',
    'VA',
    'VT',
    'WA',
]
# States we cannot operate in.
BLOCKED_STATES_NAMES = {
    'AL': "Alabama",
    'AZ': "Arizona",
    'DE': "Delaware",
    'FL': "Florida",
    'GA': "Georgia",
    'HI': "Hawaii",
    'IA': "Iowa",
    'ID': "Idaho",
    'IL': "Illinois",
    'IN': "Indiana",
    'LA': "Louisiana",
    'MO': "Missouri",
    'MT': "Montana",
    'NV': "Nevada",
    'TX': "Texas",
    'VA': "Virginia",
    'VT': "Vermont",
    'WA': "Washington",
}

# All states, in tuple format.
# ex: [('NY', 'NY'), ('FL', 'FL'), ...]
STATE_CHOICES = [(x, x) for x in ALL_STATES]

# States it is legal to play DFS in.
LEGAL_STATES = set(ALL_STATES) - set(BLOCKED_STATES)

# Country codes we are allowed to operate in. These are in our geoip database.
LEGAL_COUNTRIES = ['US']


# State Age Limitations
DEFAULT_AGE_LIMIT = 18
# These states are differnet than the default.
STATE_AGE_EXCEPTIONS = {
    'AL': 19,
    'MA': 21,
    'NE': 19,
    'NV': 21,
}

# Build up a dictionary that will default all states to the default, unless they
# exist in state_age_exceptions.
# ex: {'AK': 18, 'AL': 19, 'AR': 18, ...}
STATE_AGE_LIMITS = {}
for state in ALL_STATES:
    if state in STATE_AGE_EXCEPTIONS:
        STATE_AGE_LIMITS[state] = STATE_AGE_EXCEPTIONS[state]
    else:
        STATE_AGE_LIMITS[state] = DEFAULT_AGE_LIMIT
