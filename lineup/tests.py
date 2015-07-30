from test.classes import AbstractTest
from test.models import PlayerChild
from .classes import LineupManager
from test.classes import BuildWorldForTesting
import lineup.exceptions
from draftgroup.models import Player
from django.contrib.contenttypes.models import ContentType
from .models import Lineup, Player as LineupPlayer
from datetime import timedelta, time
from django.utils import timezone
class LineupTest(AbstractTest):
    def setUp(self):


        self.world = BuildWorldForTesting()
        self.world.build_world()
        self.draftgroup = self.world.draftgroup


        self.user = self.get_basic_user()

        self.one = PlayerChild.objects.filter(position =self.world.position1)[0]
        self.two = PlayerChild.objects.filter(position=self.world.position2)[0]
        self.three = PlayerChild.objects.filter(position=self.world.position1)[1]
        self.four = PlayerChild.objects.filter(position=self.world.position2)[1]

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
            i+=1

        #
        # edit test
        team = [self.three.pk, self.two.pk, self.one.pk]
        lm.edit_lineup(team, lineup)

        lineup_players = LineupPlayer.objects.filter(lineup=lineup).order_by('idx')
        i = 0
        for lineup_player in lineup_players:
            self.assertEqual(lineup_player.player_id, team[i])
            i+=1

    def test_bad_player_ids(self):
        lm = LineupManager(self.user)
        self.assertRaises(PlayerChild.DoesNotExist,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk, 9999], self.draftgroup))

    def test_bad_too_small_lineup(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.InvalidLineupSizeException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk], self.draftgroup))

    def test_bad_too_large_lineup(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.InvalidLineupSizeException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk, self.three.pk, self.four.pk], self.draftgroup))

    def test_invalid_position(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.LineupInvalidRosterSpotException,
                          lambda: lm.create_lineup([self.one.pk, self.three.pk,  self.two.pk], self.draftgroup))


    def test_invalid_salary_player(self):
        lm = LineupManager(self.user)
        c_type = ContentType.objects.get_for_model(self.one)
        draftgroup_player = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=self.one.pk,
                                               draft_group=self.draftgroup)
        draftgroup_player.delete()
        self.assertRaises(lineup.exceptions.PlayerDoesNotExistInDraftGroupException,
                          lambda: lm.create_lineup([self.one.pk, self.two.pk,  self.three.pk], self.draftgroup))

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
                          lambda: lm.create_lineup([self.one.pk, self.two.pk,  self.three.pk], self.draftgroup))



    def test_swap_player_for_active(self):
        self.create_valid_lineup()
        team = [self.one.pk, self.two.pk, self.four.pk]

        #
        # TEST swap active for inactive
        c_type = ContentType.objects.get_for_model(self.four)
        draftgroup_player_four = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=self.four.pk,
                                               draft_group=self.draftgroup)
        draftgroup_player_four.start = timezone.now() - timedelta(minutes=1)
        draftgroup_player_four.save()


        self.assertRaises(lineup.exceptions.PlayerSwapGameStartedException,
                          lambda: self.lm.edit_lineup(team, self.lineup))
        #
        # TEST swap active for active
        c_type = ContentType.objects.get_for_model(self.three)
        draftgroup_player_three = Player.objects.get(salary_player__player_type=c_type,
                                               salary_player__player_id=self.three.pk,
                                               draft_group=self.draftgroup)
        draftgroup_player_three.start = timezone.now() - timedelta(minutes=1)
        draftgroup_player_three.save()

        self.assertRaises(lineup.exceptions.PlayerSwapGameStartedException,
                          lambda: self.lm.edit_lineup(team, self.lineup))

        #
        # TEST swap inactive for active
        draftgroup_player_four.start = timezone.now() + timedelta(minutes=15)
        draftgroup_player_four.save()

        self.assertRaises(lineup.exceptions.PlayerSwapGameStartedException,
                          lambda: self.lm.edit_lineup(team, self.lineup))

