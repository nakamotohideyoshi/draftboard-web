#
import sports.nba.models
from sports.sport.base_parser import AbstractDataDenParser

class AbstractParseable(object):
    def __init__(self):
        self.name = self.__class__.__name__
    def parse(self, obj, target=None):
        print( self.name, str(obj)[:200], 'target='+str(target) )

class GameSchedule(AbstractParseable):
    def __init__(self):
        super().__init__()

class GameStats(AbstractParseable):
    def __init__(self):
        super().__init__()

class PlayerStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        o = obj.get_o()
        srid_game = o.get('game__id', None)
        srid_player = o.get('id', None)

        try:
            ps = sports.nba.models.PlayerStats.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.nba.models.PlayerStats.DoesNotExist:
            ps = sports.nba.models.PlayerStats()
            ps.srid_game    = srid_game
            ps.srid_player  = srid_player
            ps.save()
        return ps

class PlayerPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class EventPbp(AbstractParseable):
    def __init__(self):
        super().__init__()

class DataDenNba(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.nba.models.Game

    def parse(self, obj):
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # nba.game
        if self.target == ('nba.game','schedule'): GameSchedule().parse( obj )
        elif self.target == ('nba.game','stats'): GameStats().parse( obj )
        #
        # nba.player
        elif self.target == ('nba.player','stats'): PlayerStats().parse( obj )
        elif self.target == ('nba.player','pbp'): PlayerPbp().parse( obj )
        #
        # nba.event
        elif self.target == ('nba.event','pbp'): EventPbp().parse( obj )
        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
