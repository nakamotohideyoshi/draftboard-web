#
# sports/nhl/tests.py

from test.classes import AbstractTest
from django.test import TestCase
from datetime import datetime
from django.utils import timezone
from dataden.watcher import OpLogObj
from sports.nhl.parser import EventPbp
from ast import literal_eval
import sports.nhl.models

class TestEventPbp(AbstractTest):
    """
    test parse an actual object which once came from dataden. (sanity check)

    there is a more generic test in sports.sport.tests
    """

    def setUp(self):
        self.obj_str = """{'o': {'parent_list__id': 'events__list', 'description': 'Kris Letang shot blocked by Tyler Seguin', 'id': '6c55cd4a-ceef-4a16-ad25-92295246e1b0', 'event_type': 'shotmissed', '_id': 'cGFyZW50X2FwaV9faWRwYnBnYW1lX19pZDg2NDViYzQ0LWEyYmYtNDkyYi1hMGU3LTg1MDAyYWM2OTc4Y3BlcmlvZF9faWQ4NTY4OGVmZS0zN2YxLTRjOTMtYmE3MS00YzA1NmQ2MTk5NzJwYXJlbnRfbGlzdF9faWRldmVudHNfX2xpc3RpZDZjNTVjZDRhLWNlZWYtNGExNi1hZDI1LTkyMjk1MjQ2ZTFiMA==', 'zone': 'offensive', 'dd_updated__id': 1444379408289, 'statistics__list': {'block__list': {'player': '42ea7555-0f24-11e2-8525-18a905767e44', 'strength': 'even', 'team': '44157522-0f24-11e2-8525-18a905767e44'}, 'attemptblocked__list': {'player': '4342422b-0f24-11e2-8525-18a905767e44', 'strength': 'even', 'team': '4417b7d7-0f24-11e2-8525-18a905767e44'}}, 'parent_api__id': 'pbp', 'period__id': '85688efe-37f1-4c93-ba71-4c056d619972', 'clock': '5:47', 'attribution': '4417b7d7-0f24-11e2-8525-18a905767e44', 'updated': '2015-10-09T01:12:33+00:00', 'location__list': {'coord_x': 1683.0, 'coord_y': 282.0}, 'game__id': '8645bc44-a2bf-492b-a0e7-85002ac6978c'}, 'ns': 'nhl.event', 'ts': 1454659978}"""
        self.data = literal_eval(self.obj_str) # convert to dict
        self.oplog_obj = OpLogObj(self.data)

        # the field we will try to get a game srid from
        self.game_srid_field        = 'game__id'
        # a list of the game_srids we expect to get back (only 1 for this test)
        self.target_game_srids      = ['8645bc44-a2bf-492b-a0e7-85002ac6978c']

        # the field name we will search for player srid(s)
        self.player_srid_field      = 'player'
        # the list of player srids we expect to find in this object
        self.target_player_srids    = ['4342422b-0f24-11e2-8525-18a905767e44']

        self.player_stats_class     = sports.nhl.models.PlayerStats

    def test_event_pbp_parse(self):
        """
        """
        event_pbp = EventPbp()
        event_pbp.parse(self.oplog_obj)

        game_srids = event_pbp.get_srids_for_field(self.game_srid_field)
        self.assertIsInstance( game_srids, list )
        self.assertEquals( set(game_srids), set(self.target_game_srids) )
        self.assertEquals( len(set(game_srids)), 1 )

        # we are going to use the game_srid for a PlayerStats filter()
        game_srid = list(set(game_srids))[0]
        self.assertIsInstance( game_srid, str ) # the srid should be a string

        # we are going to use the list of player srids for the PlayerStats filter()
        player_srids = event_pbp.get_srids_for_field(self.player_srid_field)
        #print('player_srids', player_srids)
        self.assertTrue( set(self.target_player_srids) <= set(player_srids) )