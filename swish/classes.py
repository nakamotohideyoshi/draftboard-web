from logging import getLogger
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

logger = getLogger('swish.classes')


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
        name = swish_update.get_player_name()
        # try to get this player using the PlayerLookup (if the model is set)
        # otherwise falls back on simple name-matching
        player_srid = self.get_srid_for(pid=pid, name=name)  # TODO catch self.PlayerDoesNotExist

        # internally calls super().update(player_srid, *args, **kwargs)
        update_id = swish_update.get_update_id()
        # updated_at = swish_update.get_updated_at()

        # hard code this to use the category: 'injury' for testing
        category = 'injury'
        type = 'rotowire'
        value = swish_update.get_field(UpdateData.field_text) # not used due to no data from rotowire

        # get status
        status = swish_update.get_field(UpdateData.field_swish_status, 'unknown')
        # get source_origin
        # source_origin = swish_update.get_field(UpdateData.field_source_origin, 'unknown')
        source_origin = 'rotowire'
        # get url_origin
        # url_origin = swish_update.get_field(UpdateData.field_url_origin, '')
        url_origin = 'https://rotowire.com'

        # roster_status = swish_update.get_field(UpdateData.field_roster_status)
        # roster_status_description = swish_update.get_field(UpdateData.field_roster_status_description)
        # depth_chart_status = swish_update.get_field(UpdateData.field_depth_chart_status)
        # player_status_probability = swish_update.get_field(UpdateData.field_player_status_probability, 0)
        # player_status_confidence = swish_update.get_field(UpdateData.field_player_status_confidence, 0)
        # last_text = swish_update.get_field(UpdateData.field_last_text)
        # game_id = swish_update.get_field(UpdateData.field_game, {}).get('gameId', 0) #???

        # create a PlayerUpdate model in the db.

        kwargs = {
            'published_at': datetime.now(),
            # 'roster_status': roster_status,
            # 'roster_status_description': roster_status_description,
            # 'depth_chart_status': depth_chart_status,
            # 'player_status_probability': player_status_probability,
            # 'player_status_confidence': player_status_confidence,
            # 'last_text': last_text,
            # 'game_id': game_id,
            'sport': self.sport
        }

        update_obj = self.add(
            player_srid,
            update_id,
            category,
            type,
            # value,
            status,
            source_origin,
            url_origin,
            **kwargs

        )
        return update_obj


class UpdateData(object):
    """ wrapper for each update object. this class is constructed with the JSON of an individual update """

    field_update_id = 'SportsDataId'

    field_datetime_utc = 'datetimeUtc'  # ???

    field_position = 'Position'  # the sport position, ie: 'QB', 'TE' , etc...

    field_text = 'text'  # ???
    field_sport = 'sport'  # ???

    field_player_id = 'id'
     # "SportsDataId": "b1b2d578-44df-4e05-9884-31dd89e82cf0",

    field_player_first_name = 'FirstName'  # its the first name
    field_player_last_name = 'LastName'  # its the last name

    field_source = 'source'  # ???
    field_source_origin = 'sourceOrigin'  # ???  # ie: rotowire, twitter, etc...


    field_swish_status = 'InjuryStatus'


    field_url_origin = 'urlOrigin'  # ???  # for twitter, the url to the post
    field_roster_status = 'rosterStatus'   # ???
    field_roster_status_description = 'rosterStatusDescription'  # ???
    field_depth_chart_status = 'depthChartStatus'  # ???
    field_player_status_probability = 'playerStatusProbability'  # ???
    field_player_status_confidence = 'playerStatusConfidence'  # ???
    field_last_text = 'lastText'  # ???
    field_game = 'game'  # ???


    def __init__(self, data):
        self.data = data

    def get_field(self, field, default=None):
        """
        get the named field. the default return value can be specified
         in the case that a None value would be found.

        :param field:
        :param default:
        :return:
        """
        return self.data.get(field, default)

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

    def get_player_name(self):
        """ lowercases, and returns the full players name. """
        return '{} {}'.format(self.data.get(self.field_player_first_name),
                              self.data.get(self.field_player_last_name))


class SwishAnalytics(object):
    """
    api example:

        https://api.swishanalytics.com/nfl/players/injuries?date=2016-08-15,2016-08-16&team=ne&apikey=XXXXXXXX

    """

    class SwishApiException(Exception):
        pass

    # known swish status id(s) and their string names
    STARTING, ACTIVE, PROBABLE, GAMETIME_DECISION, QUESTIONABLE, DOUBTFUL, OUT, DAY_TO_DAY, WEEK_TO_WEEK, \
    MONTH_TO_MONTH, OUT_FOR_SEASON, WAIVED, TRADED = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14
    # range(1, 15) but for some reason here no 12 didn't find any description in docs
    statuses = [
        (STARTING, 'starting'),
        (ACTIVE, 'active'),
        (PROBABLE, 'probable'),
        (GAMETIME_DECISION, 'gametime-decision'),
        (QUESTIONABLE, 'questionable'),
        (DOUBTFUL, 'doubtful'),
        (OUT, 'out'),
        (DAY_TO_DAY, 'day-to-day'),
        (WEEK_TO_WEEK, 'week-to-week'),
        (MONTH_TO_MONTH, 'month-to-month'),
        (OUT_FOR_SEASON, 'out-for-season'),
        (WAIVED, 'waived'),
        (TRADED, 'traded'),
    ]

    # we will save the api call response in this table
    history_model_class = History

    api_base_url = 'https://api.swishanalytics.com'
    api_injuries = '/players/injuries'
    api_projections_game = '/players/fantasy'
    api_projections_season = '/players/fantasy/remaining'  # exists also: '/players/fantasy/season'
    api_player_status = '/players/status'

    api_key = settings.SWISH_API_KEY

    sport = None

    extra_player_fields = [
        'rosterStatus',
        'rosterStatusDescription',
        'depthChartStatus',
        'playerStatusProbability',
        'playerStatusConfidence',
        'lastText',
        'game',
    ]

    def __init__(self, sport):
        # create the Session object for performing the api calls
        self.session = requests.Session()
        # always hold onto the last http response
        self.r = None
        # the list of updates (UpdateData objects) if it has been parsed will be set here
        self.updates = None
        self.sport = sport

    def get_sport(self):
        return self.sport

    # def save_history(self, response):
    #     """ save the http_status and the JSON of the response in the database """
    #     history = self.history_model_class()
    #     history.http_status = response.status_code
    #     try:
    #         data = json.loads(response.text)
    #     except ValueError:
    #         # set a default value because the History model cant set None for the data
    #         data = {}
    #
    #     history.data = data
    #     history.save()
    #     # we could raise exception if we could not parse anything in the body of the request

    def call_api(self, url):
        """ retrieve the api as json """
        logger.info('swish url: %s' % url)
        self.r = self.session.get(url)

        # save the response in the database
        # self.save_history(self.r)

        # otherwise convert it to JSON and return the the data
        return json.loads(self.r.text)

    def get_formatted_date(self):
        """ returns a formatted date string like: '2016-08-16' """
        now = datetime.now()
        return str(now.date())

    def get_player_extra_data(self, player_id, team):
        url = '%s/%s%s?playerId=%s&team=%s&apikey=%s' % (self.api_base_url, self.sport,
                                                         self.api_player_status, player_id, team, self.api_key)
        response_data = self.call_api(url)
        results = response_data.get('data', {}).get('results', [])
        if results:
            data = results[0]
            return {x: data.get(x) for x in self.extra_player_fields}
        else:
            return {}

    def get_updates(self):
        formatted_date = self.get_formatted_date()
        url = '%s/%s%s?date=%s&apikey=%s' % (self.api_base_url, self.sport,
                                             self.api_injuries, formatted_date, self.api_key)
        response_data = self.call_api(url)


        # results will be a list of the updates from swish
        results = response_data.get('data', {}).get('results', [])
        self.updates = []
        for update_data in results:
            status = update_data.get('swishStatusId')
            if status == self.STARTING:
                extra_data = self.get_player_extra_data(update_data.get('playerId'), update_data.get('teamId'))
                update_data.update(extra_data)
            self.updates.append(UpdateData(update_data))

        logger.info('%s UpdateData(s)' % len(self.updates))

        return self.updates


class RotoWire(object):
    """
    api example:

        http://api.rotowire.com/Basketball/NBA/Injuries.php?key=XXXXXXXX&format=json

    """

    class RotoWireApiException(Exception):
        pass

    # known swish status id(s) and their string names
    STARTING, ACTIVE, PROBABLE, GAMETIME_DECISION, QUESTIONABLE, DOUBTFUL, OUT, DAY_TO_DAY, WEEK_TO_WEEK, \
    MONTH_TO_MONTH, OUT_FOR_SEASON, WAIVED, TRADED = 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14
    # range(1, 15) but for some reason here no 12 didn't find any description in docs
    statuses = [
        (STARTING, 'starting'),
        (ACTIVE, 'active'),
        (PROBABLE, 'probable'),
        (GAMETIME_DECISION, 'gtd'),
        (QUESTIONABLE, 'questionable'),
        (DOUBTFUL, 'doubtful'),
        (OUT, 'out'),
        (DAY_TO_DAY, 'day-to-day'),
        (WEEK_TO_WEEK, 'week-to-week'),
        (MONTH_TO_MONTH, 'month-to-month'),
        (OUT_FOR_SEASON, 'out-for-season'),
        (WAIVED, 'waived'),
        (TRADED, 'traded'),
    ]

    # we will save the api call response in this table
    history_model_class = History

    api_base_url = 'http://api.rotowire.com'
    api_injuries = 'Injuries.php'
    api_news = 'News.php'
    # api_projections_game = '/players/fantasy'
    # api_projections_season = '/players/fantasy/remaining'  # exists also: '/players/fantasy/season'
    # api_player_status = '/players/status'

    # api_key = settings.SWISH_API_KEY
    api_key = settings.ROTOWIRE_API_KEY

    sport = None

    # extra_player_fields = [
    #     'rosterStatus',
    #     'rosterStatusDescription',
    #     'depthChartStatus',
    #     'playerStatusProbability',
    #     'playerStatusConfidence',
    #     'lastText',
    #     'game',
    # ]

    def __init__(self, sport):
        # create the Session object for performing the api calls
        self.session = requests.Session()
        # always hold onto the last http response
        self.r = None
        # the list of updates (UpdateData objects) if it has been parsed will be set here
        self.updates = None
        self.sport = sport

    def get_sport(self):
        return self.sport

    # def save_history(self, response):
    #     """ save the http_status and the JSON of the response in the database """
    #     history = self.history_model_class()
    #     history.http_status = response.status_code
    #     try:
    #         data = json.loads(response.text)
    #     except ValueError:
    #         # set a default value because the History model cant set None for the data
    #         data = {}
    #
    #     history.data = data
    #     history.save()
    #     # we could raise exception if we could not parse anything in the body of the request

    def call_api(self, url):
        """ retrieve the api as json """
        logger.info('swish url: %s' % url)
        self.r = self.session.get(url)

        # save the response in the database
        # self.save_history(self.r)

        # otherwise convert it to JSON and return the the data
        return json.loads(self.r.text)

    def get_formatted_date(self):
        """ returns a formatted date string like: '2016-08-16' """
        now = datetime.now()
        return str(now.date())

    def get_player_extra_data(self):
        url = '{}/Basketball/{}/{}?key={}&format=json'.format(self.api_base_url, self.sport, self.api_news,
                                                              self.api_key)
        response_data = self.call_api(url)
        results = response_data.get('Updates', {})
        if results:

            data = results
            return {str(update.get('Player').get('Id')): '{} {}'.format(update.get('Notes'), update.get('Analysis')) for update in data}
        else:
            return {}

    def get_updates(self):
        formatted_date = self.get_formatted_date()
        url = '{}/Basketball/{}/{}?key={}&format=json'.format(self.api_base_url, self.sport, self.api_injuries,  self.api_key)
        response_data = self.call_api(url)
        text_data = self.get_player_extra_data()
        # results will be a list of the updates from swish
        results = response_data.get('Players', {})
        self.updates = []
        for update_data in results:
            update_data['text'] = text_data.get(str(update_data.get('id')))
            self.updates.append(UpdateData(update_data))

        logger.info('%s UpdateData(s)' % len(self.updates))
        return self.updates
