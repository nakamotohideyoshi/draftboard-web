from test.classes import AbstractTest
from test.models import PlayerChild
from .classes import LineupManager
from test.classes import BuildWorldForTesting
import lineup.exceptions

class LineupTest(AbstractTest):
    def setUp(self):


        self.world = BuildWorldForTesting()
        self.world.build_world()
        self.draftgroup = self.world.draftgroup


        self.user = self.get_basic_user()

        self.one = PlayerChild.objects.filter(position =self.world.position1)[0]
        self.two = PlayerChild.objects.filter(position=self.world.position2)[0]
        self.three = PlayerChild.objects.filter(position=self.world.position1)[1]

    def test_create_lineup(self):
        lm = LineupManager(self.user)
        lm.create_lineup([self.one.pk, self.two.pk, self.three.pk], self.draftgroup)

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
                          lambda: lm.create_lineup([self.one.pk, self.two.pk, self.three.pk, self.three.pk], self.draftgroup))

    def test_invalid_position(self):
        lm = LineupManager(self.user)
        self.assertRaises(lineup.exceptions.LineupInvalidRosterSpotException,
                          lambda: lm.create_lineup([self.one.pk, self.three.pk,  self.two.pk], self.draftgroup))