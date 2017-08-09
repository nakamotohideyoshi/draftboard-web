from logging import getLogger
import requests
import json
import dateutil
from django.conf import settings
from django.db.transaction import atomic
from datetime import datetime, date, timedelta

from swish.exception import RotowireDownException
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
    def update(self, rotowire_update):
        """
        override. update this third party data and enter it as a PlayerUpdate

        :param swish_update:
        """
        # get rotowire sports data id
        player_srid = rotowire_update.get_srid()

        # internally calls super().update(player_srid, *args, **kwargs)
        update_id = rotowire_update.get_update_id()

        # hard code this to use the category: 'injury' for testing
        # category = 'injury'
        category = rotowire_update.get_field('category')
        type = 'rotowire'
        value = rotowire_update.get_text() # latest news
        notes = rotowire_update.get_notes()
        analysis = rotowire_update.get_analysis()
        headline = rotowire_update.get_headline()

        # get status
        status = rotowire_update.get_injury_status()
        # get source_origin
        source_origin = 'rotowire'
        # get url_origin
        url_origin = 'https://rotowire.com'

        # create a PlayerUpdate model in the db.

        kwargs = {
            'published_at': rotowire_update.get_updated_at(),
            'sport': self.sport,
            'notes': notes,
            'analysis': analysis,
            'headline': headline,
        }

        update_obj = self.add(
            player_srid,
            update_id,
            category,
            type,
            value,
            status,
            source_origin,
            url_origin,
            **kwargs

        )
        return update_obj


class UpdateData(object):
    """ wrapper for each update object. this class is constructed with the JSON of an individual update """

    field_category = 'category'
    field_update_id = 'Id'

    field_datetime_utc = 'DateTime'  # ???

    field_position = 'Position'  # the sport position, ie: 'QB', 'TE' , etc...

    field_notes = 'Notes'  # ???
    field_analysis = 'Analysis'  # ???
    field_headline = 'Headline'  # ???
    field_sport = 'sport'  # ???

    field_player = 'Player'
    field_player_id = 'Id'
    field_player_srid = 'SportsDataId'

    field_player_first_name = 'FirstName'  # its the first name
    field_player_last_name = 'LastName'  # its the last name

    field_source = 'source'  # ???
    field_source_origin = 'sourceOrigin'  # ???  # ie: rotowire, twitter, etc...

    field_injury = 'Injury'
    field_injury_status = 'Status'

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
        if self.data.get(self.field_datetime_utc):
            parsed = dateutil.parser.parse(self.data.get(self.field_datetime_utc))
            new_format = parsed.strftime('%Y-%m-%d %H:%M:%S')
            dt_str = '%s UTC' % new_format
            return dateutil.parser.parse(dt_str, tzinfos={'UTC': UtcTime.TZ_UTC})

    def get_update_id(self):
        """ converts the update id to a str, and returns it """
        return str(self.data.get(self.field_update_id))

    def get_sport(self):
        """ lowercases, and returns the sport like: 'nfl', 'mlb', etc... """
        return self.data.get(self.field_sport).lower()

    def get_player_name(self):
        """  returns the full players name. """
        return '{} {}'.format(self.data.get(self.field_player).get(self.field_player_first_name),
                              self.data.get(self.field_player).get(self.field_player_last_name))

    def get_pid(self):
        """  returns the players id. """
        return self.data.get(self.field_player).get(self.field_player_id)

    def get_srid(self):
        """  returns the players srid. """
        return self.data.get(self.field_player).get(self.field_player_srid)

    def get_text(self):
        """ returns the news text. """
        return '{} {}'.format(self.data.get(self.field_notes),
                              self.data.get(self.field_analysis))

    def get_notes(self):
        """ returns the news notes. """
        return self.data.get(self.field_notes, '')

    def get_analysis(self):
        """ returns the news field_analysis. """
        return self.data.get(self.field_analysis, '')

    def get_headline(self):
        """ returns the news field_analysis. """
        return self.data.get(self.field_headline, '')

    def get_injury_status(self):
        """ returns injury status. """
        if self.get_sport() == 'mlb':
            status = self.data.get(self.field_player).get(self.field_injury).get(self.field_injury_status) or 'active'
        else:
            status = self.data.get(self.field_injury).get(self.field_injury_status) or 'active'

        return status


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
    NBA = 'nba'
    MLB = 'mlb'
    NHL = 'nhl'
    NFL = 'nfl'
    SPORTS = {
        NBA: 'Basketball',
        MLB: 'Baseball',
        NFL: 'Football',
        NHL: 'Hockey',
    }

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
    api_players = 'Players.php'
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
        if self.r.status_code == 200:
            return self.r.json()
        else:
            raise RotowireDownException(self.r)

    def get_formatted_date(self):
        """ returns a formatted date string like: '2016-08-16' """
        now = datetime.now()
        return str(now.date())

    def get_injuries(self):
        url = '{}/{}/{}/{}?key={}&format=json'.format(
            self.api_base_url,
            self.SPORTS.get(self.sport),
            self.sport,
            self.api_injuries,
            self.api_key
        )
        response_data = self.call_api(url)
        results = response_data.get('Players', {})
        self.updates = []

        for update_data in filter(lambda x: x.get('SportsDataId'), results):
            data = {}
            data['Id'] = update_data.get('Id')
            data['category'] = 'injury'
            data['sport'] = self.sport
            data['Player'] = {}
            data['Player']['Id'] = update_data.get('Id')
            data['Player']['SportsDataId'] = update_data.get('SportsDataId')
            data['Player']['FirstName'] = update_data.get('FirstName')
            data['Player']['LastName'] = update_data.get('LastName')
            if self.sport == 'mlb':
                data['Player']['Injury'] = {}
                data['Player']['Injury']['Status'] = update_data.get('Injury').get('Status')
            else:
                data['Injury'] = {}
                data['Injury']['Status'] = update_data.get('Injury').get('Status')
            self.updates.append(UpdateData(data))

        logger.info('%s UpdateData(s)' % len(self.updates))
        return self.updates

    def get_news(self):
        formatted_date = self.get_formatted_date()
        url = '{}/{}/{}/{}?key={}&format=json&hours=24'.format(
            self.api_base_url,
            self.SPORTS.get(self.sport),
            self.sport,
            self.api_news,
            self.api_key
        )
        response_data = self.call_api(url)
        # results will be a list of the updates from swish
        results = response_data.get('Updates', {})
        self.updates = []
        for update_data in filter(lambda x: x.get('Player').get('SportsDataId'), results):
            update_data['category'] = 'news'
            update_data['sport'] = self.sport
            self.updates.append(UpdateData(update_data))

        logger.info('%s UpdateData(s)' % len(self.updates))
        return self.updates

    def get_players(self):
        url = '{}/{}/{}/{}?key={}&format=json'.format(
            self.api_base_url,
            self.SPORTS.get(self.sport),
            self.sport,
            self.api_players,
            self.api_key
        )
        response_data = self.call_api(url)
        # free players
        players_data = []
        # add players
        [players_data.extend(x.get('Players')) for x in response_data.get('Teams', [])]
        return filter(lambda x: x.get('SportsDataId'), players_data)


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

    def get_player_extra_data_multiple(self, player_id):
        url = '%s/%s%s?playerId=%s&apikey=%s' % (self.api_base_url, self.sport,
                                                             self.api_player_status, player_id, self.api_key)

        response_data = self.call_api(url)
        results = response_data.get('data', {}).get('results', [])
        if results:
            return results
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