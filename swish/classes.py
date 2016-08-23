#
# classes.py

import time
import requests
import json
import dateutil
from django.conf import settings
from django.db.transaction import atomic
from datetime import datetime, date, timedelta
from util.utctime import UtcTime
import draftgroup.classes
from swish.models import (
    History,
    PlayerLookup,
)

class PlayerUpdateManager(draftgroup.classes.PlayerUpdateManager):
    """
    Swish Analytics own class for injecting PlayerUpdate objects into the backend
    particularly so they show up in /api/draft-group/updates/{draft-group-id}/
    """

    # model class for looking up player -> third party id mappings set by admin
    lookup_model_class = PlayerLookup

    @atomic
    def update(self, swish_update):
        """
        override. update this third party data and enter it as a PlayerUpdate

        :param swish_update:
        """

        # get the players' swish id
        pid = swish_update.get_field(UpdateData.field_player_id)
        name = swish_update.get_field(UpdateData.field_player_name)

        # try to get this player using the PlayerLookup (if the model is set)
        # otherwise falls back on simple name-matching
        player_srid = self.get_srid_for(pid=pid, name=name) # TODO catch self.PlayerDoesNotExist

        # internally calls super().update(player_srid, *args, **kwargs)
        update_id = swish_update.get_update_id()
        updated_at = swish_update.get_updated_at()

        # hard code this to use the category: 'injury' for testing
        category = 'injury'
        type = swish_update.get_field(UpdateData.field_source)
        value = swish_update.get_field(UpdateData.field_text)

        # create a PlayerUpdate model in the db.
        update_obj = self.add(
            player_srid,
            update_id,
            category,
            type,
            value,
            published_at=updated_at
        )
        return update_obj

class UpdateData(object):
    """ wrapper for each update object. this class is constructed with the JSON of an individual update """

    field_update_id = 'id'
    field_datetime_utc = 'datetimeUtc'
    field_position = 'position'             # the sport position, ie: 'QB', 'TE' , etc...
    field_text = 'text'
    field_sport = 'sport'
    field_player_id = 'playerId'
    field_player_name = 'playerName'        # its the full name
    field_source = 'source'
    field_source_origin = 'sourceOrigin'    # ie: rotowire, twitter, etc...
    field_swish_status = 'swishStatus'      # ie: 'week-to-week', etc...

    def __init__(self, data):
        self.data = data

    def get_field(self, field):
        return self.data.get(field)

    def get_updated_at(self):
        """
        we know the datetimeUtc is in utc, so append " UTC" and use dateutil to
        return a datetime object that has its tzinfo properly set

        example dateutil.parser usage:

            In [34]: parser.parse("2016-08-16 22:11:55 UTC", tzinfos={'UTC':UtcTime.TZ_UTC})
            Out[34]: datetime.datetime(2016, 8, 16, 22, 11, 55, tzinfo=<UTC>)

        """
        dt_str = '%s UTC' % self.data.get(self.field_datetime_utc)
        return dateutil.parser.parse(dt_str, tzinfos={'UTC': UtcTime.TZ_UTC})

    def get_update_id(self):
        """ converts the update id to a str, and returns it """
        return str(self.data.get(self.field_update_id))

    def get_sport(self):
        """ lowercases, and returns the sport like: 'nfl', 'mlb', etc... """
        return self.data.get(self.field_sport).lower()

class SwishAnalytics(object):
    """
    api example:

        https://api.swishanalytics.com/nfl/players/injuries?date=2016-08-15,2016-08-16&team=ne&apikey=XXXXXXXX

    """

    class SwishApiException(Exception): pass

    # known swish status id(s) and their string names
    statuses = [
        (1, 'starting'),
        (2, 'active'),
        (3, 'probable'),
        (4, 'gametime-decision'),
        (5, 'questionable'),
        (6, 'doubtful'),
        (7, 'out'),
        (8, 'day-to-day'),
        (9, 'week-to-week'),
        (10, 'month-to-month'),
        (11, 'out-for-season'),
        (13, 'waived'),
        (14, 'traded'),
    ]

    # we will save the api call response in this table
    history_model_class = History

    api_base_url = 'https://api.swishanalytics.com'
    api_injuries = '/players/injuries'
    api_projections_game = '/players/fantasy'
    api_projections_season = '/players/fantasy/remaining'   # exists also: '/players/fantasy/season'

    api_key = settings.SWISH_API_KEY

    sport = None

    def __init__(self):
        # create the Session object for performing the api calls
        self.session = requests.Session()
        # always hold onto the last http response
        self.r = None
        # the list of updates (UpdateData objects) if it has been parsed will be set here
        self.updates = None

    def get_sport(self):
        return self.sport

    def save_history(self, response):
        """ save the http_status and the JSON of the response in the database """
        history = self.history_model_class()
        history.http_status = response.status_code
        try:
            data = json.loads(response.text)
        except ValueError:
            # set a default value because the History model cant set None for the data
            data = {}

        history.data = data
        history.save()
        # TODO raise exception if we could not parse anything in the body of the request

    def call_api(self, url):
        """ retrieve the api as json """
        print('swish url:', str(url))
        self.r = self.session.get(url)

        # save the response in the database
        #self.save_history(self.r)

        # otherwise convert it to JSON and return the the data
        return json.loads(self.r.text)

    def get_formatted_date(self):
        """ returns a formatted date string like: '2016-08-16' """
        now = datetime.now()
        return str(now.date())

    def get_updates(self):
        formatted_date = self.get_formatted_date()
        url = '%s/%s%s?date=%s&apikey=%s' % (self.api_base_url, self.sport,
                                            self.api_injuries, formatted_date, self.api_key)
        response_data = self.call_api(url)

        # results will be a list of the updates from swish
        results = response_data.get('data',{}).get('results',[])
        self.updates = []
        for update_data in results:
            self.updates.append(UpdateData(update_data))

        print('%s UpdateData(s)' % str(len(self.updates)))

        return self.updates

class SwishNFL(SwishAnalytics):
    sport = 'nfl'

class SwishNHL(SwishAnalytics):
    sport = 'nhl'

class SwishNBA(SwishAnalytics):
    sport = 'nba'

class SwishMLB(SwishAnalytics):
    sport = 'mlb'