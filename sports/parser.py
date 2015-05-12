#

import sports.nba.parser
import sports.mlb.parser

class DataDenParser(object):
    """
    returns a parser for a sport
    """
    NAMESPACE = 'ns'

    parsers = {
        'nba' : sports.nba.parser.DataDenNba,
        'mlb' : sports.mlb.parser.DataDenMlb,
    }

    def __init__(self):
        self.sport = None

    @staticmethod
    def get_for_sport(sport):
        """
        get the parser for a specific sport by its string name

        :param sport:
        :return:
        """
        parser = DataDenParser.parsers.get( sport, None )
        if parser is None:
            raise Exception('parser does not exist for sport: ' + str(sport))

        return parser()

    def get_sport_from_namespace(self, obj):
        ns = obj.get_ns()
        return ns.split('.')[0] # sport always on the left side of the dot

    def __get_parser(self, sport):
        dataden_sport_parser = self.parsers[ sport ]
        return dataden_sport_parser()

    def parse(self, obj):
        """
        inspect the namespace of the object, and pass it to the proper sport parser
        """
        self.sport = self.get_sport_from_namespace( obj )
        parser = self.__get_parser( self.sport )
        parser.parse( obj ) # the sub parser will infer what type of object it is

class ProviderParser(object):
    """
    get an object that can parse our providers objects
    """
    parsers = {
        'dataden' : DataDenParser,

        # ... implement and add more providers here
    }

    @staticmethod
    def get_for_provider(provider):
        provider_parser = ProviderParser.parsers.get(provider, None)
        if provider_parser is None:
            raise Exception('provider_parser [%s] does not exist' % str(provider))

        return provider_parser()

