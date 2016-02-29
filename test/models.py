#
# test/models.py

from django.db import models
from transaction.models import TransactionDetail, Balance
from sports.models import Game, PlayerStats, Player, Team
from lineup.models import Lineup

#
# Test models must be created outside of the tests
class TransactionDetailChild(TransactionDetail):
    pass

class BalanceChild(Balance):
    pass

class TeamChild(Team):

    class Meta:
        abstract = False

    def __str__(self):
        return super().__str__()

class GameChild(Game):

    home = models.ForeignKey( TeamChild, null=True, related_name='gamechild_hometeam')
    srid_home   = models.CharField(max_length=64, null=True,
                                help_text='home team sportsradar global id')

    away = models.ForeignKey( TeamChild, null=True, related_name='gamechild_awayteam')
    srid_away   = models.CharField(max_length=64, null=True,
                                help_text='away team sportsradar global id')
    title       = models.CharField(max_length=128, null=True)

    class Meta:
        abstract = False

    def __str__(self):
        return super().__str__()

class PlayerChild(Player):

    team    = models.ForeignKey( TeamChild, null=True )

    class Meta:
        abstract = False

    def __str__(self):
        return super().__str__()

class PlayerStatsChild(PlayerStats):

    class Meta:
        abstract = False

    #
    # use parent's fantasy_points property

    def __str__(self):
        return super().__str__()

# class LineupWithFantasyPoints( Lineup ):
#
#     # override for the final fantasy points to bypass the scorer,
#     # especially so that tests do not need to incorporate
#     # the DraftGroup method for finalizing the sum of the fantasy points
#     # so we can more easily test payouts.
#     #
#     # this model mimics every other behavior of a Lineup model
#     # except that it always returns the self.test_fantasy_points
#     # when get_test_fantasy_points() is called
#     test_fantasy_points = 10.0
#
#     def get_test_fantasy_points(self):
#         return self.test_fantasy_points
#
#     class Meta:
#         proxy = True



