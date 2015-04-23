#from enum import Enum

#
# these are the states which are not allowed to play daily fantasy
# Arizona(AZ), Iowa(IA), Montana(MT), Washington(WA)

#
# currently these are the U.S. states which allow daily fantasy players.

# the legal states. the strange gaps are for the illegal states
states = [
    'AL','AK',     'AR','CA','CO','CT','DE','FL','GA',
    'HI','ID','IL','IN',     'KS','KY','LA','ME','MD',
    'MA','MI','MN','MS','MO',     'NE','NV','NH','NJ',
    'NM','NY','NC','ND','OH','OK','OR','PA','RI','SC',
    'SD','TN','TX','UT','VT','VA',     'WV','WI','WY'
]

#
# generated from the 'states' list !
state_choices = [ (x, x) for x in states ]