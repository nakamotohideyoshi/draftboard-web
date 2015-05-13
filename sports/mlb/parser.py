#
#
import sports.mlb.models
from sports.sport.base_parser import AbstractDataDenParser

class AbstractParseable(object):
    def __init__(self):
        self.name = self.__class__.__name__
    def parse(self, obj, target=None):
        print( self.name, str(obj)[:100], 'target='+str(target) )

class GameSchedule(AbstractParseable):
    def __init__(self):
        super().__init__()

class GameStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

class PlayerStats(AbstractParseable):
    def __init__(self):
        super().__init__()
    def parse(self, obj, target=None):
        super().parse( obj, target )

        o = obj.get_o()
        srid_game = o.get('game__id', None)
        srid_player = o.get('id', None)

        try:
            ps = sports.mlb.models.PlayerStats.objects.get( srid_game=srid_game, srid_player=srid_player )
        except sports.mlb.models.PlayerStats.DoesNotExist:
            ps = sports.mlb.models.PlayerStats()
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

class DataDenMlb(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.mlb.models.Game

    def parse(self, obj):
        super().parse( obj ) # setup self.ns, self.parent_api

        #
        # game
        if self.target == ('mlb.game','schedule_reg'): GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pre'): GameSchedule().parse( obj )
        elif self.target == ('mlb.game','schedule_pst'): GameSchedule().parse( obj )
        #
        elif self.target == ('mlb.game','summary'): GameStats().parse( obj )

        #
        # player
        elif self.target == ('mlb.player','summary'): PlayerStats().parse( obj )

        #
        # default case, print this message for now
        else: self.unimplemented( self.target[0], self.target[1] )
