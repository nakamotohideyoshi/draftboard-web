#
# test/models.py

from django.db import models
from transaction.models import TransactionDetail, Balance
import sports.models
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

class Season( sports.models.Season ):
    """

    """
    class Meta:
        abstract = False

class GameChild(Game):

    # the season field for actual sports all set null=False
    # but setting this to allow None will save a lot of tests from breaking
    season      = models.ForeignKey(Season, null=True)

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




