#
#

import sports.models
from sports.parser import AbstractDataDenParser

class DataDenNba(AbstractDataDenParser):

    def __init__(self):
        self.game_model = sports.models.NbaGame

    def game(self, o):
        """
        parse a game from a dataden object into our local database
        o is a hashable object !

        :param o:
        :return:
        """

        print( '%s.game()' % self.name(), str(o) )