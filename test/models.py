from transaction.models import TransactionDetail, Balance
from sports.models import Game, PlayerStats, Player



#
# Test models must be created outside of the test
# class
class TransactionDetailChild(TransactionDetail):
    pass

class BalanceChild(Balance):
    pass


class GameChild(Game):
    pass

class PlayerChild(Player):
    pass

class PlayerStatsChild(PlayerStats):
    pass