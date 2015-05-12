#
# sports/sport/base_parser.py

class AbstractDataDenParser(object):
    """
    for parsing each individual sport, which will have some differences
    """
    game_model = None

    def __init__(self):
        self.validate_models()

        self.ns         = None
        self.parent_api = None

    def validate_models(self):
        if self.game_model is None:
            raise Exception('game_model is not set')

    def name(self):
        """
        helper method to get the class name of the instance, mainly for logging
        :return:
        """
        return self.__class__.__name__

    def unimplemented(self, ns, parent_api):
        print('UNIMPLEMENTED <<< %s | %s >>>' % (ns,parent_api))

    def parse(self, obj):
        self.ns         = obj.get_ns()
        self.parent_api = obj.get_parent_api()
        self.target     = (self.ns, self.parent_api)

        print ('%s.parse() | %s %s %s' % ( self.name(),
               self.ns, self.parent_api, str(obj.get_o()) ) )
        #
        # child parse() will execute here -- they must call super().parse( obj )
        #  then this class will have setup self.ns and self.parent_api for them