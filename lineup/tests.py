from datetime import timedelta

from django.contrib.contenttypes.models import ContentType
from django.test.utils import override_settings  # for testing celery
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

import lineup.exceptions
import test.classes
from contest.models import Entry
from draftgroup.models import Player
from lineup.views import (
    CreateLineupAPIView,
)
from test.classes import AbstractTest
from test.classes import BuildWorldForTesting
from test.models import PlayerChild
from .classes import LineupManager
from .models import Player as LineupPlayer
from .tasks import edit_lineup, edit_entry


# Notes:
# rest_framework.status has these helper methods (which all return a boolean):
# is_informational()  # 1xx
# is_success()        # 2xx
# is_redirect()       # 3xx
# is_client_error()   # 4xx
# is_server_error()   # 5xx

class CreateLineupAPITest(APITestCase,
                          test.classes.BuildWorldMixin,
                          test.classes.ForceAuthenticateAndRequestMixin):
    def setUp(self):
        super().setUp()
        """
        1. builds the world
        2. logs in a newly created user

        """
        # build world, and create a user with username='user'
        self.build_world()
        self.user = self.create_user('user')

    def test_create_lineup_invalid_params(self):
        data = {
            'draft_group_id': "asdf",
            'players': "['steve', 9999]",
        }
        url = '/api/lineup/create/'
        response = self.force_authenticate_and_POST(self.user, CreateLineupAPIView, url, data)

        # is_client_error() checks any 400 errors (401, 402, etc...)
        self.assertTrue(status.is_client_error(response.status_code))


class BuildWorldMixin(object):
    """
    inherit this class in a TestCase with the intent to call build_world() in the setUp() method.

    usage:

         class LineupTest(AbstractTest, BuildWorldMixin):

            def setUp(self):
                self.build_world()

            def test_something_with_with_the_world(self):
                pass # perform some test ...

    """

    def build_world(self):
        self.world = BuildWorldForTesting()
        self.world.build_world()
        self.draftgroup = self.world.draftgroup

        self.user = self.get_basic_user()

        self.one = PlayerChild.objects.filter(position=self.world.position1, team__name="test1")[0]
        self.two = PlayerChild.objects.filter(position=self.world.position2, team__name="test3")[0]
        self.three = PlayerChild.objects.filter(position=self.world.position1, team__name="test2")[
            0]
        self.four = PlayerChild.objects.filter(position=self.world.position2, team__name="test2")[0]

        team = [self.one, self.two, self.three]
        for player in team:
            c_type = ContentType.objects.get_for_model(player)
            draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                                   salary_player__player_id=player.pk,
                                                   draft_group=self.draftgroup)
            draftgroup_player.salary = 10000
            draftgroup_player.save()

    def create_valid_lineup(self):
        self.lm = LineupManager(self.user)
        self.team = [self.one.pk, self.two.pk, self.three.pk]
        self.lineup = self.lm.create_lineup(self.team, self.draftgroup)


class LineupTest(AbstractTest, BuildWorldMixin):
    def setUp(self):
        super().setUp()
        self.build_world()

    def test_create_and_edit_lineup(self):
        #
        # create test
        lm = LineupManager(self.user)
        team = [self.one.pk, self.two.pk, self.three.pk]
        lineup = lm.create_lineup(team, self.draftgroup)

        lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')

        i = 0
        for lineup_player in lineup_players:
            self.assertEqual(lineup_player.player_id, team[i])
            i += 1

        #
        # edit test
        team = [self.three.pk, self.two.pk, self.one.pk]
        lm.edit_lineup(team, lineup)

        lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')
        i = 0
        for lineup_player in lineup_players:
            self.assertEqual(lineup_player.player_id, team[i])
            i += 1

    def test_create_lineup_past_time(self):
        #
        # move the draftgroup time
        self.draftgroup.start = timezone.now() - timedelta(minutes=1)
        self.draftgroup.save()

        lm = LineupManager(self.user)
        team = [self.one.pk, self.two.pk, self.three.pk]

        self.assertRaises(lineup.exceptions.CreateLineupExpiredDraftgroupException,
                          lambda: lm.create_lineup(team, self.draftgroup))

    def test_bad_too_small_lineup(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.InvalidLineupSizeException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk], self.draftgroup))

    def test_bad_too_large_lineup(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.InvalidLineupSizeException,
                          lambda: lm.create_lineup(
                              [self.one.pk, self.two.pk, self.three.pk, self.four.pk],
                              self.draftgroup))

    def test_invalid_position(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.LineupInvalidRosterSpotException,
                          lambda: lm.create_lineup([self.one.pk, self.three.pk, self.two.pk],
                                                   self.draftgroup))

    def test_invalid_salary_player(self):
        lm = LineupManager(self.user)
        c_type = ContentType.objects.get_for_model(self.one)
        draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=self.one.pk,
                                               draft_group=self.draftgroup)
        draftgroup_player.delete()
        self.assertRaises(lineup.exceptions.PlayerDoesNotExistInDraftGroupException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk, self.three.pk],
                                                   self.draftgroup))

    def test_too_large_of_team_salary(self):
        lm = LineupManager(self.user)

        lm = LineupManager(self.user)
        c_type = ContentType.objects.get_for_model(self.one)
        draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=self.one.pk,
                                               draft_group=self.draftgroup)
        draftgroup_player.salary = 1000000
        draftgroup_player.save()
        self.assertRaises(lineup.exceptions.InvalidLineupSalaryException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk, self.three.pk],
                                                   self.draftgroup))

    def test_edit_entry_past_start(self):
        self.create_valid_lineup()
        #
        # move the draftgroup time
        self.draftgroup.start = timezone.now() - timedelta(minutes=1)
        self.draftgroup.save()

        lm = LineupManager(self.user)
        team = [self.one.pk, self.two.pk, self.three.pk]
        entry = Entry()
        entry.lineup = self.lineup
        entry.contest = self.world.contest
        entry.user = self.user
        entry.save()

        self.assertRaises(lineup.exceptions.CreateLineupExpiredDraftgroupException,
                          lambda: lm.edit_entry(team, entry))

    def test_edit_lineup_past_start(self):
        self.create_valid_lineup()
        #
        # move the draftgroup time
        self.draftgroup.start = timezone.now() - timedelta(minutes=1)
        self.draftgroup.save()

        lm = LineupManager(self.user)
        team = [self.one.pk, self.two.pk, self.three.pk]

        self.assertRaises(lineup.exceptions.CreateLineupExpiredDraftgroupException,
                          lambda: lm.edit_lineup(team, self.lineup))

    def test_edit_entry_same_lineup(self):
        self.create_valid_lineup()

        team = [self.one.pk, self.two.pk, self.three.pk]
        entry = Entry()
        entry.lineup = self.lineup
        entry.contest = self.world.contest
        entry.user = self.user
        entry.save()

        self.assertRaises(lineup.exceptions.LineupUnchangedException,
                          lambda: self.lm.edit_entry(team, entry))

    def test_edit_entry_split_lineup(self):
        self.create_valid_lineup()

        team = [self.one.pk, self.two.pk, self.four.pk]
        entry = Entry()
        entry.lineup = self.lineup
        entry.contest = self.world.contest
        entry.user = self.user
        entry.save()

        entry2 = Entry()
        entry2.lineup = self.lineup
        entry2.contest = self.world.contest
        entry2.user = self.user
        entry2.save()

        self.lm.edit_entry(team, entry)

        entry.refresh_from_db()
        lineup_players = LineupPlayer.objects.get(lineup=entry.lineup, idx=2)
        lineup_players2 = LineupPlayer.objects.get(lineup=entry2.lineup, idx=2)

        self.assertNotEquals(lineup_players.pk, lineup_players2.pk)

    def test_edit_entry_single(self):
        self.create_valid_lineup()

        team = [self.one.pk, self.two.pk, self.four.pk]
        entry = Entry()
        entry.lineup = self.lineup
        entry.contest = self.world.contest
        entry.user = self.user
        entry.save()

        self.lm.edit_entry(team, entry)
        entry.refresh_from_db()

        self.assertEquals(entry.lineup.pk, self.lineup.pk)

    """
    Disabled because we've changed to 1 lineup per draftgroup, this means there cna be no lineup
    merging.
    """

    # def test_merge_lineups_create(self):
    #     self.create_valid_lineup()
    #
    #     team = [self.one.pk, self.two.pk, self.three.pk]
    #     entry = Entry()
    #     entry.lineup = self.lineup
    #     entry.contest = self.world.contest
    #     entry.user = self.user
    #     entry.save()
    #
    #     entry2 = Entry()
    #     entry2.lineup = self.lineup
    #     entry2.contest = self.world.contest
    #     entry2.user = self.user
    #     entry2.save()
    #
    #     new_lineup = self.lm.create_lineup(team, self.draftgroup)
    #     entry.refresh_from_db()
    #     entry2.refresh_from_db()
    #
    #     self.assertEquals(entry.lineup.pk, new_lineup.pk)
    #     self.assertEquals(entry2.lineup.pk, new_lineup.pk)
    #
    #     self.assertRaises(Lineup.DoesNotExist,
    #                       lambda: Lineup.objects.get(pk=self.lineup.pk))

    # def test_merge_lineups_edit(self):
    #     self.create_valid_lineup()
    #
    #     team = [self.one.pk, self.two.pk, self.four.pk]
    #     new_lineup = self.lm.create_lineup(team, self.draftgroup)
    #     self.assertNotEquals(self.lineup.pk, new_lineup.pk)
    #
    #     team = [self.one.pk, self.two.pk, self.three.pk]
    #
    #     entry = Entry()
    #     entry.lineup = self.lineup
    #     entry.contest = self.world.contest
    #     entry.user = self.user
    #     entry.save()
    #
    #     entry2 = Entry()
    #     entry2.lineup = new_lineup
    #     entry2.contest = self.world.contest
    #     entry2.user = self.user
    #     entry2.save()
    #
    #     self.lm.edit_lineup(team, entry2.lineup)
    #     entry.refresh_from_db()
    #
    #     self.assertEquals(entry.lineup.pk, new_lineup.pk)
    #
    #     self.assertRaises(Lineup.DoesNotExist,
    #                       lambda: Lineup.objects.get(pk=self.lineup.pk))

    def test_get_lineup_from_id(self):
        self.create_valid_lineup()
        #
        # Tests the future to make sure that we dont give user lineups
        # before a contest starts
        self.draftgroup.start = timezone.now() + timedelta(minutes=1)
        self.draftgroup.save()

        lm = LineupManager(self.user)
        data = lm.get_lineup_from_id(self.lineup.pk, self.world.contest)
        for player_obj_arr in data:
            self.assertEquals(player_obj_arr['started'], False)
            self.assertEquals(player_obj_arr['data'], [])

        #
        # Tests the future to make sure that we show all players as started
        self.draftgroup.start = timezone.now() - timedelta(minutes=1)
        self.draftgroup.save()

        lm = LineupManager(self.user)
        data = lm.get_lineup_from_id(self.lineup.pk, self.world.contest)
        for player_obj_arr in data:
            self.assertEquals(player_obj_arr['started'], True)

    def test_two_lineups_in_draftgroup(self):
        lm = LineupManager(self.user)
        team = [self.one.pk, self.two.pk, self.four.pk]
        lineup_1 = lm.create_lineup(team, self.draftgroup)

        self.assertRaises(
            lineup.exceptions.DraftgroupLineupLimitExceeded,
            lambda: lm.create_lineup(team, self.draftgroup))


class LineupConcurrentTest(AbstractTest, BuildWorldMixin):
    def setUp(self):
        super().setUp()
        self.build_world()

    @override_settings(CELERYD_CONCURRENCY=3)
    def test_edit_lineup_as_task(self):
        self.create_valid_lineup()
        team = [self.one.pk, self.two.pk, self.four.pk]

        def run_test(user, team, lineup):
            task = edit_lineup.delay(user, team, lineup)
            self.assertFalse(task.successful())

        task = edit_lineup.delay(self.user, team, self.lineup)
        # Don't run them concurrently here because it's broken and needs to be fixed.
        # self.concurrent_test(3, run_test, self.user, team, self.lineup)
        self.assertEqual(task.state, 'SUCCESS')
        self.assertTrue(task.successful())

    @override_settings(CELERYD_CONCURRENCY=3)
    def test_edit_entry_as_task(self):
        self.create_valid_lineup()
        entry = Entry()
        entry.lineup = self.lineup
        entry.contest = self.world.contest
        entry.user = self.user
        entry.save()

        team = [self.one.pk, self.two.pk, self.four.pk]

        def run_test(user, team, entry):
            task = edit_entry.delay(user, team, entry)
            self.assertFalse(task.successful())

        task = edit_entry.delay(self.user, team, entry)
        # self.concurrent_test(3, run_test, self.user, team, entry)
        self.assertEqual(task.state, 'SUCCESS')
        self.assertTrue(task.successful())
